from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Patient(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients', help_text="Doctor responsible for this patient")
    history_of_illness = models.CharField(max_length=10, unique=True, help_text="Medical history number (unique identifier)")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField()
    phone_validator = RegexValidator(
        regex=r'^[\d\s\+\-\(\)]{1,20}$',
        message="Phone number can contain digits, spaces, +, -, ( )"
    )
    phone_number = models.CharField(validators=[phone_validator], max_length=20, default='0')
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
    @property
    def full_name(self):
        if self.patronymic:
            return f"{self.first_name} {self.patronymic} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='history')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'Patient Name History'
        verbose_name_plural = 'Patient Name History'
    
    def __str__(self):
        if self.patronymic:
            return f"{self.first_name} {self.patronymic} {self.last_name} ({self.changed_at.strftime('%Y-%m-%d')})"
        return f"{self.first_name} {self.last_name} ({self.changed_at.strftime('%Y-%m-%d')})"
