from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Measurement, MeasurementValue
from .serializers import MeasurementSerializer, RadarChartDataSerializer
from .forms import MeasurementForm
from patients.models import Patient
from indicators.models import Indicator
from authentication.decorators import (
    active_staff_required, can_view_all_patients_required, 
    can_edit_patients_required, can_delete_data_required, 
    can_view_analytics_required
)


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    
    def get_queryset(self):
        # Filter measurements to only show those for current doctor's patients
        queryset = Measurement.objects.filter(patient__doctor=self.request.user)
        patient_id = self.request.query_params.get('patient', None)
        show_in_chart = self.request.query_params.get('show_in_chart', None)
        
        if patient_id is not None:
            queryset = queryset.filter(patient_id=patient_id)
        if show_in_chart is not None:
            queryset = queryset.filter(show_in_chart=show_in_chart.lower() == 'true')
            
        return queryset.select_related('patient').prefetch_related('values__indicator')

    @action(detail=False, methods=['get'])
    def hexagon_chart_data(self, request):
        """Get hexagon chart data for a specific patient grouped by schemas"""
        patient_id = request.query_params.get('patient_id')
        if not patient_id:
            return Response({'error': 'patient_id parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        patient = get_object_or_404(Patient, id=patient_id, doctor=request.user)
        
        # Get all active schemas with their indicators
        from indicators.models import Schema
        schemas = Schema.objects.filter(is_active=True).prefetch_related(
            'indicators'
        ).order_by('order')
        
        schemas_data = []
        
        for schema in schemas:
            # Get schema indicators
            schema_indicators = schema.indicators.filter(is_active=True).order_by('name')
            
            # Get measurements for this patient that have values for this schema
            measurements = Measurement.objects.filter(
                patient=patient,
                show_in_chart=True,
                values__indicator__schema=schema
            ).prefetch_related('values__indicator').distinct().order_by('-measurement_date')
            
            measurements_data = []
            for measurement in measurements:
                measurement_values = []
                total_score = 0
                
                for indicator in schema_indicators:
                    value_obj = measurement.values.filter(indicator=indicator).first()
                    if value_obj:
                        score = max(0, min(2, value_obj.value))
                        measurement_values.append({
                            'indicator_name': indicator.name,
                            'value': score,
                            'max': 2
                        })
                        total_score += score
                    else:
                        measurement_values.append({
                            'indicator_name': indicator.name,
                            'value': 0,
                            'max': 2
                        })
                
                measurements_data.append({
                    'id': measurement.id,
                    'date': measurement.measurement_date.strftime('%Y-%m-%d'),
                    'values': measurement_values,
                    'total_score': total_score
                })
            
            # Calculate risk level using recommendation templates from database
            latest_measurement = measurements_data[0] if measurements_data else None
            risk_info = None
            
            if latest_measurement:
                total_score = latest_measurement['total_score']
                max_score = len(schema_indicators) * 2
                
                # Find matching recommendation template from database
                from indicators.models import RecommendationTemplate
                recommendation = RecommendationTemplate.objects.filter(
                    schema=schema,
                    min_score__lte=total_score,
                    max_score__gte=total_score
                ).first()
                
                if recommendation:
                    risk_info = {
                        'level': recommendation.risk_level,
                        'text': recommendation.get_risk_level_display(),
                        'range': f'{recommendation.min_score}-{recommendation.max_score} баллов',
                        'title': recommendation.title,
                        'description': recommendation.description,
                        'recommendations': recommendation.recommendations
                    }
                else:
                    # Fallback if no template found
                    risk_info = {'level': 'low', 'text': 'Нет данных о риске', 'range': ''}
            
            schema_data = {
                'id': schema.id,
                'name': schema.name,
                'description': schema.description,
                'indicators': [{
                    'id': ind.id,
                    'name': ind.name,
                    'min_value': ind.min_value,
                    'max_value': ind.max_value
                } for ind in schema_indicators],
                'measurements': measurements_data,
                'risk_info': risk_info
            }
            
            schemas_data.append(schema_data)
        
        response_data = {
            'patient_id': patient.id,
            'patient_name': patient.full_name,
            'schemas': schemas_data
        }
        
        response = Response(response_data)
        # Prevent caching
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    @action(detail=False, methods=['get'])
    def schema_arithmetic_mean(self, request):
        """Calculate arithmetic mean for all patients by schema"""
        schema_id = request.query_params.get('schema_id')
        if not schema_id:
            return Response({'error': 'schema_id parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        from indicators.models import Schema
        schema = get_object_or_404(Schema, id=schema_id, is_active=True)
        
        # Get all measurements for all patients for this schema
        measurements = Measurement.objects.filter(
            show_in_chart=True,
            values__indicator__schema=schema
        ).prefetch_related('values__indicator').distinct()
        
        # Calculate arithmetic mean for each indicator in the schema
        schema_indicators = schema.indicators.filter(is_active=True).order_by('name')
        mean_values = []
        
        for indicator in schema_indicators:
            # Get all values for this indicator across all patients
            values = []
            for measurement in measurements:
                for value in measurement.values.filter(indicator=indicator):
                    # Ensure value is within 0-2 range
                    chart_value = max(0, min(2, value.value))
                    values.append(chart_value)
            
            if values:
                mean_value = sum(values) / len(values)
                mean_values.append({
                    'indicator_name': indicator.name,
                    'mean_value': round(mean_value, 2),
                    'sample_size': len(values)
                })
            else:
                mean_values.append({
                    'indicator_name': indicator.name,
                    'mean_value': 0,
                    'sample_size': 0
                })
        
        response_data = {
            'schema_id': schema.id,
            'schema_name': schema.name,
            'total_patients': measurements.values('patient').distinct().count(),
            'total_measurements': measurements.count(),
            'mean_values': mean_values
        }
        
        response = Response(response_data)
        # Prevent caching
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    
    @action(detail=False, methods=['get'])
    def scoring_ranges(self, request):
        """Get scoring ranges for indicators"""
        from indicators.models import ScoringRange
        
        indicator_id = request.query_params.get('indicator_id')
        if not indicator_id:
            return Response({'error': 'indicator_id parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        ranges = ScoringRange.objects.filter(indicator_id=indicator_id).order_by('score')
        
        ranges_data = []
        for scoring_range in ranges:
            range_data = {
                'score': scoring_range.score,
                'description': scoring_range.description,
                'min_value': scoring_range.min_value,
                'max_value': scoring_range.max_value,
                'is_greater_than_or_equal': scoring_range.is_greater_than_or_equal,
                'is_less_than': scoring_range.is_less_than,
                'exact_value': scoring_range.exact_value,
            }
            ranges_data.append(range_data)
        
        return Response({'indicator_id': indicator_id, 'ranges': ranges_data})
    
    
    


@can_view_analytics_required
def radar_chart_view(request, patient_id):
    """Template view for radar chart"""
    patient = get_object_or_404(Patient, id=patient_id, doctor=request.user)
    context = {
        'patient': patient,
        'patient_id': patient_id
    }
    return render(request, 'measurements/radar_chart.html', context)


@can_view_all_patients_required
def patient_list(request):
    """List all patients with links to their charts"""
    from django.core.paginator import Paginator
    
    # Get page size from request, default to 5
    page_size = int(request.GET.get('size', 5))
    if page_size not in [5, 10, 50]:
        page_size = 5
    
    # Get page number from request
    page_number = request.GET.get('page', 1)
    
    # Get all patients for current doctor with measurement count
    all_patients = Patient.objects.filter(doctor=request.user).annotate(
        measurement_count=models.Count('measurements')
    ).order_by('last_name', 'first_name')
    
    # Create paginator
    paginator = Paginator(all_patients, page_size)
    patients_page = paginator.get_page(page_number)
    
    # Calculate status for each patient based on their latest measurement scores
    for patient in patients_page:
        # Get latest measurement for this patient
        latest_measurement = Measurement.objects.filter(
            patient=patient,
            show_in_chart=True
        ).order_by('-measurement_date').first()
        
        if latest_measurement:
            # Calculate total score from all measurement values
            total_score = sum(
                mv.value for mv in latest_measurement.values.all()
            )
            # Get max possible score (number of indicators * 2)
            max_score = latest_measurement.values.count() * 2
            
            if max_score > 0:
                score_percentage = (total_score / max_score) * 100
                
                # Determine status based on score percentage
                if score_percentage <= 33:  # 0-33% = Low risk (Green)
                    patient.status = 'low'
                    patient.status_text = 'Низкий риск'
                    patient.status_color = 'success'
                elif score_percentage <= 66:  # 34-66% = Medium risk (Yellow)
                    patient.status = 'medium'
                    patient.status_text = 'Средний риск'
                    patient.status_color = 'warning'
                else:  # 67-100% = High risk (Red)
                    patient.status = 'high'
                    patient.status_text = 'Высокий риск'
                    patient.status_color = 'danger'
                
                patient.total_score = total_score
                patient.max_score = max_score
            else:
                patient.status = 'no_data'
                patient.status_text = 'Нет данных'
                patient.status_color = 'secondary'
        else:
            patient.status = 'no_data'
            patient.status_text = 'Нет измерений'
            patient.status_color = 'secondary'
    
    total_patients = Patient.objects.filter(doctor=request.user).count()
    showing_count = len(patients_page)
    
    context = {
        'patients': patients_page,
        'patients_page': patients_page,
        'paginator': paginator,
        'page_size': page_size,
        'total_patients': total_patients,
        'showing_count': showing_count,
        'current_page': page_number
    }
    return render(request, 'measurements/patient_list.html', context)


@active_staff_required
def dashboard(request):
    """Dashboard home page"""
    recent_measurements = Measurement.objects.filter(patient__doctor=request.user).select_related('patient').order_by('-created_at')[:10]
    total_patients = Patient.objects.filter(doctor=request.user).count()
    total_measurements = Measurement.objects.filter(patient__doctor=request.user).count()
    active_indicators = Indicator.objects.filter(is_active=True).count()
    
    context = {
        'recent_measurements': recent_measurements,
        'total_patients': total_patients,
        'total_measurements': total_measurements,
        'active_indicators': active_indicators,
    }
    return render(request, 'measurements/dashboard.html', context)


@can_edit_patients_required
def add_measurement(request, patient_id):
    """Add measurement for specific patient"""
    patient = get_object_or_404(Patient, id=patient_id, doctor=request.user)
    schema_id = request.GET.get('schema')
    
    if request.method == 'POST':
        form = MeasurementForm(request.POST, patient_id=patient_id, schema_id=schema_id)
        if form.is_valid():
            measurement = form.save()
            messages.success(request, 'Measurement added successfully!')
            return redirect('radar_chart', patient_id=patient.id)
    else:
        form = MeasurementForm(patient_id=patient_id, schema_id=schema_id)
    
    # Debug: print form fields
    indicators = Indicator.objects.filter(is_active=True).order_by('name')
    print("DEBUG: Available indicators:")
    for ind in indicators:
        print(f"  - '{ind.name}' (ID: {ind.id})")
    
    print("DEBUG: Form fields:")
    for field_name, field in form.fields.items():
        print(f"  - {field_name}: {type(field).__name__}")
    
    # Prepare indicator fields for template
    indicator_fields = []
    for indicator in indicators:
        field_name = f'indicator_{indicator.id}'
        field = form.fields.get(field_name)
        if field:
            indicator_fields.append({
                'indicator': indicator,
                'field': form[field_name],
                'field_name': field_name,
                'min_value': indicator.min_value,
                'max_value': indicator.max_value
            })
    
    context = {
        'form': form,
        'patient': patient,
        'indicators': indicators,
        'indicator_fields': indicator_fields
    }
    return render(request, 'measurements/add_measurement.html', context)


@can_edit_patients_required
def edit_measurement(request, measurement_id):
    """Edit existing measurement"""
    measurement = get_object_or_404(Measurement, id=measurement_id, patient__doctor=request.user)
    patient = measurement.patient
    
    # Get current schema from URL parameter or from measurement's indicators
    schema_id = request.GET.get('schema')
    if not schema_id:
        # Get schema from the measurement's existing indicators
        first_indicator = measurement.values.select_related('indicator__schema').first()
        if first_indicator and first_indicator.indicator.schema:
            schema_id = first_indicator.indicator.schema.id
    
    if request.method == 'POST':
        print(f"DEBUG: POST data received: {request.POST}")
        form = MeasurementForm(request.POST, instance=measurement, patient_id=patient.id, schema_id=schema_id)
        if form.is_valid():
            print(f"DEBUG: Form is valid, saving measurement {measurement.id}")
            measurement = form.save()
            print(f"DEBUG: Measurement saved successfully")
            
            # Force a database transaction commit
            from django.db import transaction
            transaction.commit()
            
            messages.success(request, 'Measurement updated successfully!')
            # Add a timestamp parameter to force chart refresh
            import time
            refresh_param = f"?updated={int(time.time())}"
            return redirect(f"/chart/{patient.id}/{refresh_param}")
        else:
            print(f"DEBUG: Form errors: {form.errors}")
            messages.error(request, f'Form validation failed: {form.errors}')
    else:
        # Pre-populate form with existing values
        initial_data = {}
        for value in measurement.values.all():
            # Get the raw value that would produce this score
            raw_value = None
            if value.indicator.name == 'Курение':
                if value.value == 0:
                    raw_value = 0
                elif value.value == 1:
                    raw_value = 10  # mid-range example
                elif value.value == 2:
                    raw_value = 25  # high-range example
            elif value.indicator.name == 'Длительность нахождения в психоневрологическом интернате':
                if value.value == 0:
                    raw_value = 3
                elif value.value == 1:
                    raw_value = 7
                elif value.value == 2:
                    raw_value = 15
            elif value.indicator.name == 'Прием препаратов, снижающих слюноотделение (антипсихотические)':
                if value.value == 0:
                    raw_value = 0
                elif value.value == 1:
                    raw_value = 1
                elif value.value == 2:
                    raw_value = 3
            elif value.indicator.name == 'Уровень комплаентности':
                if value.value == 0:
                    raw_value = 38
                elif value.value == 1:
                    raw_value = 26
                elif value.value == 2:
                    raw_value = 18
            elif value.indicator.name == 'Наличие сопутствующей соматической патологии (кол-во соматических заболеваний)':
                if value.value == 0:
                    raw_value = 0
                elif value.value == 1:
                    raw_value = 1
                elif value.value == 2:
                    raw_value = 3
            elif value.indicator.name == 'Данные анкетирования OHIP 14':
                if value.value == 0:
                    raw_value = 20
                elif value.value == 1:
                    raw_value = 35
                elif value.value == 2:
                    raw_value = 50
            else:
                raw_value = value.value
            
            initial_data[f'indicator_{value.indicator.id}'] = raw_value
        
        form = MeasurementForm(instance=measurement, patient_id=patient.id, schema_id=schema_id, initial=initial_data)
    
    # Get indicators for the selected schema only
    if schema_id:
        try:
            from indicators.models import Schema
            schema = Schema.objects.get(id=schema_id)
            indicators = schema.indicators.filter(is_active=True).order_by('name')
        except Schema.DoesNotExist:
            indicators = Indicator.objects.filter(is_active=True).order_by('name')
    else:
        indicators = Indicator.objects.filter(is_active=True).order_by('name')
    
    # Prepare indicator fields for template
    indicator_fields = []
    for indicator in indicators:
        field_name = f'indicator_{indicator.id}'
        field = form.fields.get(field_name)
        if field:
            indicator_fields.append({
                'indicator': indicator,
                'field': form[field_name],
                'field_name': field_name,
                'min_value': indicator.min_value,
                'max_value': indicator.max_value
            })
    
    context = {
        'form': form,
        'patient': patient,
        'measurement': measurement,
        'indicators': indicators,
        'indicator_fields': indicator_fields,
        'is_edit': True
    }
    return render(request, 'measurements/add_measurement.html', context)


@can_delete_data_required
def delete_measurement(request, measurement_id):
    """Delete measurement"""
    measurement = get_object_or_404(Measurement, id=measurement_id, patient__doctor=request.user)
    patient_id = measurement.patient.id
    
    if request.method == 'POST':
        measurement.delete()
        messages.success(request, 'Measurement deleted successfully!')
        return redirect('radar_chart', patient_id=patient_id)
    
    context = {
        'measurement': measurement,
        'patient': measurement.patient
    }
    return render(request, 'measurements/confirm_delete.html', context)
