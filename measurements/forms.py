from django import forms
from django.utils import timezone
from .models import Measurement, MeasurementValue
from indicators.models import Indicator, Schema
from patients.models import Patient


class MeasurementForm(forms.ModelForm):
    schema = forms.ModelChoiceField(
        queryset=Schema.objects.filter(is_active=True).order_by('order'),
        empty_label="Select Schema",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'schema-selector'}),
        help_text="Choose which indicator schema to use for this measurement"
    )
    
    class Meta:
        model = Measurement
        fields = ['patient', 'schema', 'measurement_date', 'show_in_chart', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'measurement_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'show_in_chart': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient_id', None)
        schema_id = kwargs.pop('schema_id', None)
        super().__init__(*args, **kwargs)
        
        if patient_id:
            self.fields['patient'].initial = patient_id
            self.fields['patient'].widget = forms.HiddenInput()
        
        # Set default measurement time to now
        if not self.instance.pk:
            self.fields['measurement_date'].initial = timezone.now().strftime('%Y-%m-%dT%H:%M')
        
        # Set default schema or use provided schema_id
        if schema_id:
            self.fields['schema'].initial = schema_id
        elif self.instance.pk:
            # For existing measurements, get schema from the measurement's indicators
            first_value = self.instance.values.select_related('indicator__schema').first()
            if first_value and first_value.indicator.schema:
                self.fields['schema'].initial = first_value.indicator.schema.id
        else:
            # Default to first schema for new measurements
            first_schema = Schema.objects.filter(is_active=True).order_by('order').first()
            if first_schema:
                self.fields['schema'].initial = first_schema.id
        
        # Add indicator value fields dynamically based on selected schema
        selected_schema_id = schema_id or self.data.get('schema') or self.fields['schema'].initial
        if selected_schema_id:
            try:
                schema = Schema.objects.get(id=selected_schema_id)
                indicators = schema.indicators.filter(is_active=True).order_by('name')
            except Schema.DoesNotExist:
                indicators = Indicator.objects.none()
        else:
            # If no schema selected, show indicators from first schema
            first_schema = Schema.objects.filter(is_active=True).order_by('order').first()
            indicators = first_schema.indicators.filter(is_active=True).order_by('name') if first_schema else Indicator.objects.none()
        
        # Generate dynamic help text from scoring ranges
        
        for indicator in indicators:
            field_name = f'indicator_{indicator.id}'
            scoring_field = f'score_{indicator.id}'
            
            # Generate help text from scoring ranges
            scoring_ranges = indicator.scoring_ranges.all().order_by('score')
            if scoring_ranges.exists():
                range_descriptions = [f"{sr.description}={sr.score}б" for sr in scoring_ranges]
                help_text = f'Введите значение. Автоматически: {", ".join(range_descriptions)}'
            else:
                help_text = f'Введите значение от {indicator.min_value} до {indicator.max_value}'
            
            # Create field with dynamic attributes
            self.fields[field_name] = forms.FloatField(
                label=indicator.name,
                required=False,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control indicator-input',
                    'placeholder': f'{indicator.min_value} - {indicator.max_value} {indicator.unit or ""}',
                    'data-indicator-id': indicator.id,
                    'data-indicator-name': indicator.name,
                    'data-min-value': indicator.min_value,
                    'data-max-value': indicator.max_value,
                    'onchange': 'calculateScore(this)',
                    'oninput': 'calculateScore(this)',
                    'step': '0.1' if indicator.unit not in ['сигарет', 'препаратов', 'заболеваний'] else '1',
                    'min': indicator.min_value if indicator.min_value is not None else 0,
                    'max': indicator.max_value if indicator.max_value is not None else 1000
                }),
                help_text=help_text
            )
    
    def clean_measurement_date(self):
        measurement_date = self.cleaned_data.get('measurement_date')
        if measurement_date and measurement_date > timezone.now():
            raise forms.ValidationError("Measurement date cannot be in the future.")
        return measurement_date
    
    def calculate_score(self, indicator, raw_value):
        """Calculate score based on indicator's scoring ranges and raw value"""
        if raw_value is None:
            return 0
        
        return indicator.calculate_score(raw_value)
    
    def save(self, commit=True):
        measurement = super().save(commit=commit)
        
        if commit:
            # Get the selected schema and its indicators
            selected_schema = self.cleaned_data.get('schema')
            if selected_schema:
                schema_indicators = selected_schema.indicators.filter(is_active=True)
                
                # Remove existing values that are not in the current schema
                measurement.values.exclude(indicator__in=schema_indicators).delete()
                
                # Save indicator values for the selected schema
                for indicator in schema_indicators:
                    field_name = f'indicator_{indicator.id}'
                    value = self.cleaned_data.get(field_name)
                    
                    if value is not None and value != '':
                        try:
                            raw_value = float(value)
                            
                            # Calculate score using the new method
                            calculated_score = self.calculate_score(indicator, raw_value)
                            
                            MeasurementValue.objects.update_or_create(
                                measurement=measurement,
                                indicator=indicator,
                                defaults={'value': calculated_score}
                            )
                            
                            print(f"DEBUG: Saved {indicator.name}: raw={raw_value}, score={calculated_score}")
                            
                        except (ValueError, TypeError) as e:
                            print(f"DEBUG: Error saving {indicator.name}: {e}")
                            pass  # Skip invalid values
                    else:
                        # Remove value if field is empty
                        MeasurementValue.objects.filter(
                            measurement=measurement,
                            indicator=indicator
                        ).delete()
        
        return measurement