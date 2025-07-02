from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import models
from .models import Schema, Indicator, ScoringRange
from .forms import IndicatorForm


def indicator_list(request):
    """List all indicators with management options"""
    indicators = Indicator.objects.all().order_by('name')
    
    context = {
        'indicators': indicators,
        'total_indicators': indicators.count(),
        'active_indicators': indicators.filter(is_active=True).count(),
    }
    return render(request, 'indicators/indicator_list.html', context)


def add_indicator(request):
    """Add new indicator"""
    if request.method == 'POST':
        form = IndicatorForm(request.POST)
        if form.is_valid():
            indicator = form.save()
            messages.success(request, f'Indicator "{indicator.name}" added successfully!')
            return redirect('indicator_list')
    else:
        form = IndicatorForm()
    
    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, 'indicators/add_indicator.html', context)


def edit_indicator(request, indicator_id):
    """Edit existing indicator"""
    indicator = get_object_or_404(Indicator, id=indicator_id)
    
    if request.method == 'POST':
        form = IndicatorForm(request.POST, instance=indicator)
        if form.is_valid():
            form.save()
            messages.success(request, f'Indicator "{indicator.name}" updated successfully!')
            return redirect('indicator_list')
    else:
        form = IndicatorForm(instance=indicator)
    
    context = {
        'form': form,
        'indicator': indicator,
        'is_edit': True
    }
    return render(request, 'indicators/add_indicator.html', context)


def delete_indicator(request, indicator_id):
    """Delete indicator"""
    indicator = get_object_or_404(Indicator, id=indicator_id)
    
    # Get statistics about related data that will be affected
    measurement_count = indicator.measurementvalue_set.count()
    
    if request.method == 'POST':
        indicator_name = indicator.name
        indicator.delete()
        messages.success(request, f'Indicator "{indicator_name}" deleted successfully!')
        return redirect('indicator_list')
    
    context = {
        'indicator': indicator,
        'measurement_count': measurement_count
    }
    return render(request, 'indicators/confirm_delete.html', context)


# Schema Management Views
def schema_list(request):
    """List all schemas with their indicators"""
    schemas = Schema.objects.all().order_by('order')
    
    context = {
        'schemas': schemas,
        'total_schemas': schemas.count(),
        'active_schemas': schemas.filter(is_active=True).count(),
    }
    return render(request, 'indicators/schema_list.html', context)


def add_schema(request):
    """Add new schema"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        order = request.POST.get('order', 1)
        is_active = request.POST.get('is_active') == 'on'
        
        if name:
            schema = Schema.objects.create(
                name=name,
                description=description,
                order=int(order),
                is_active=is_active
            )
            messages.success(request, f'Schema "{schema.name}" added successfully!')
            return redirect('schema_list')
        else:
            messages.error(request, 'Schema name is required.')
    
    # Get next order number
    last_schema = Schema.objects.order_by('-order').first()
    next_order = (last_schema.order + 1) if last_schema else 1
    
    context = {
        'next_order': next_order,
        'is_edit': False
    }
    return render(request, 'indicators/add_schema.html', context)


def edit_schema(request, schema_id):
    """Edit existing schema"""
    schema = get_object_or_404(Schema, id=schema_id)
    
    if request.method == 'POST':
        schema.name = request.POST.get('name', schema.name)
        schema.description = request.POST.get('description', '')
        schema.order = int(request.POST.get('order', schema.order))
        schema.is_active = request.POST.get('is_active') == 'on'
        schema.save()
        
        messages.success(request, f'Schema "{schema.name}" updated successfully!')
        return redirect('schema_list')
    
    context = {
        'schema': schema,
        'is_edit': True
    }
    return render(request, 'indicators/add_schema.html', context)


def delete_schema(request, schema_id):
    """Delete schema"""
    schema = get_object_or_404(Schema, id=schema_id)
    
    # Get statistics about related data that will be affected
    indicator_count = schema.indicators.count()
    measurement_count = 0
    for indicator in schema.indicators.all():
        measurement_count += indicator.measurementvalue_set.count()
    
    if request.method == 'POST':
        schema_name = schema.name
        schema.delete()
        messages.success(request, f'Schema "{schema_name}" deleted successfully!')
        return redirect('schema_list')
    
    context = {
        'schema': schema,
        'indicator_count': indicator_count,
        'measurement_count': measurement_count
    }
    return render(request, 'indicators/confirm_delete_schema.html', context)


def manage_scoring_ranges(request, indicator_id):
    """Manage scoring ranges for an indicator"""
    indicator = get_object_or_404(Indicator, id=indicator_id)
    scoring_ranges = indicator.scoring_ranges.all().order_by('score')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_range':
            score = int(request.POST.get('score', 0))
            description = request.POST.get('description', '')
            min_value = request.POST.get('min_value')
            max_value = request.POST.get('max_value')
            exact_value = request.POST.get('exact_value')
            is_greater_than_or_equal = request.POST.get('is_greater_than_or_equal') == 'on'
            is_less_than = request.POST.get('is_less_than') == 'on'
            
            # Convert empty strings to None
            min_value = float(min_value) if min_value else None
            max_value = float(max_value) if max_value else None
            exact_value = float(exact_value) if exact_value else None
            
            try:
                scoring_range = ScoringRange.objects.create(
                    indicator=indicator,
                    score=score,
                    description=description,
                    min_value=min_value,
                    max_value=max_value,
                    exact_value=exact_value,
                    is_greater_than_or_equal=is_greater_than_or_equal,
                    is_less_than=is_less_than
                )
                messages.success(request, f'Scoring range "{description}" added successfully!')
            except Exception as e:
                messages.error(request, f'Error creating scoring range: {str(e)}')
            
            return redirect('manage_scoring_ranges', indicator_id=indicator_id)
        
        elif action == 'delete_range':
            range_id = request.POST.get('range_id')
            try:
                scoring_range = ScoringRange.objects.get(id=range_id, indicator=indicator)
                range_description = scoring_range.description
                scoring_range.delete()
                messages.success(request, f'Scoring range "{range_description}" deleted successfully!')
            except ScoringRange.DoesNotExist:
                messages.error(request, 'Scoring range not found.')
            
            return redirect('manage_scoring_ranges', indicator_id=indicator_id)
    
    context = {
        'indicator': indicator,
        'scoring_ranges': scoring_ranges,
    }
    return render(request, 'indicators/manage_scoring_ranges.html', context)
