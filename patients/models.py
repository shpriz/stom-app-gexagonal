from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Patient(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patients', help_text="Врач, ответственный за этого пациента", verbose_name="Врач")
    history_of_illness = models.CharField(max_length=10, unique=True, help_text="Номер истории болезни (уникальный идентификатор)", verbose_name="Номер истории болезни")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    phone_validator = RegexValidator(
        regex=r'^[\d\s\+\-\(\)]{1,20}$',
        message="Номер телефона может содержать цифры, пробелы, +, -, ( )"
    )
    phone_number = models.CharField(validators=[phone_validator], max_length=20, default='0', verbose_name="Номер телефона")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(blank=True, verbose_name="Адрес")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
    
    @property
    def full_name(self):
        if self.patronymic:
            return f"{self.first_name} {self.patronymic} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='history', verbose_name="Пациент")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name="Изменено")
    changed_by = models.CharField(max_length=100, blank=True, verbose_name="Изменено пользователем")
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name = 'История имени пациента'
        verbose_name_plural = 'История имен пациентов'
    
    def __str__(self):
        if self.patronymic:
            return f"{self.first_name} {self.patronymic} {self.last_name} ({self.changed_at.strftime('%Y-%m-%d')})"
        return f"{self.first_name} {self.last_name} ({self.changed_at.strftime('%Y-%m-%d')})"
