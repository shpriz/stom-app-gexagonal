from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['history_of_illness', 'first_name', 'last_name', 'patronymic', 'date_of_birth', 'phone_number', 'email', 'address']
        widgets = {
            'history_of_illness': forms.TextInput(attrs={
                'class': 'form-control', 
                'maxlength': '10', 
                'placeholder': 'Medical history number (required)',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patronymic (optional)'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optional)'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Address (optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.existing_patient = None
        super().__init__(*args, **kwargs)
        
    def clean_history_of_illness(self):
        history_number = self.cleaned_data.get('history_of_illness')
        
        if not history_number:
            raise ValidationError("Medical history number is required.")
        
        # Check if patient with this history number already exists for this doctor
        # Only check if we're creating a new patient (not editing)
        if not self.instance.pk and self.user:
            try:
                existing_patient = Patient.objects.get(history_of_illness=history_number, doctor=self.user)
                self.existing_patient = existing_patient
                raise ValidationError(
                    f"Patient with history number '{history_number}' already exists: "
                    f"{existing_patient.full_name} (DOB: {existing_patient.date_of_birth}). "
                    f"Would you like to edit this patient instead?"
                )
            except Patient.DoesNotExist:
                pass  # This is good - no duplicate found
                
        return history_number
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")
        return date_of_birth