from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['history_of_illness', 'last_name', 'first_name', 'patronymic', 'date_of_birth']
        widgets = {
            'history_of_illness': forms.TextInput(attrs={
                'class': 'form-control', 
                'maxlength': '10', 
                'placeholder': 'Номер истории болезни',
                'required': True
            }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Отчество (необязательно)'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.existing_patient = None
        super().__init__(*args, **kwargs)
        
    def clean_history_of_illness(self):
        history_number = self.cleaned_data.get('history_of_illness')
        
        if not history_number:
            raise ValidationError("Номер истории болезни обязателен.")
        
        # Check if patient with this history number already exists for this doctor
        # Only check if we're creating a new patient (not editing)
        if not self.instance.pk and self.user:
            try:
                existing_patient = Patient.objects.get(history_of_illness=history_number, doctor=self.user)
                self.existing_patient = existing_patient
                raise ValidationError(
                    f"Пациент с номером '{history_number}' уже существует: "
                    f"{existing_patient.full_name} ({existing_patient.date_of_birth.strftime('%d.%m.%Y')})"
                )
            except Patient.DoesNotExist:
                pass  # This is good - no duplicate found
                
        return history_number
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth and date_of_birth > timezone.now().date():
            raise ValidationError("Дата рождения не может быть в будущем.")
        return date_of_birth