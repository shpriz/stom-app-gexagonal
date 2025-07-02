from django import forms
from .models import Schema, Indicator


class IndicatorForm(forms.ModelForm):
    class Meta:
        model = Indicator
        fields = ['schema', 'name', 'description', 'min_value', 'max_value', 'green_threshold', 'yellow_threshold', 'unit', 'is_active']
        widgets = {
            'schema': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Indicator name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description (optional)'}),
            'min_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Minimum value'}),
            'max_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Maximum value'}),
            'green_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'placeholder': 'Green zone %', 'min': '0', 'max': '100'}),
            'yellow_threshold': forms.NumberInput(attrs={'class': 'form-control', 'step': '1', 'placeholder': 'Yellow zone %', 'min': '0', 'max': '100'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit (e.g., points, mm, %)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }