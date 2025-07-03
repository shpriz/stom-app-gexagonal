from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from patients.models import Patient
from indicators.models import Indicator


class Measurement(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='measurements', verbose_name="Пациент")
    measurement_date = models.DateTimeField(verbose_name="Дата измерения")
    notes = models.TextField(blank=True, verbose_name="Заметки")
    show_in_chart = models.BooleanField(default=True, help_text="Показывать это измерение на радарной диаграмме", verbose_name="Показывать на диаграмме")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        ordering = ['-measurement_date']
        unique_together = ['patient', 'measurement_date']
        verbose_name = "Измерение"
        verbose_name_plural = "Измерения"
    
    def __str__(self):
        return f"{self.patient.full_name} - {self.measurement_date.strftime('%Y-%m-%d %H:%M')}"
    
    def get_values_dict(self):
        """Return measurement values as dict {indicator_name: value}"""
        return {
            mv.indicator.name: mv.value 
            for mv in self.values.all()
        }
    
    def get_chart_data(self):
        """Return data formatted for radar chart"""
        values = self.values.select_related('indicator').all()
        return [
            {
                'indicator': mv.indicator.name,
                'value': mv.value,
                'max_value': mv.indicator.max_value,
                'color_zone': mv.indicator.get_zone_color(mv.value),
                'unit': mv.indicator.unit
            }
            for mv in values
        ]


class MeasurementValue(models.Model):
    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='values', verbose_name="Измерение")
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, verbose_name="Индикатор")
    value = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)], help_text="Значение балла (0-2 балла)", verbose_name="Значение")
    
    class Meta:
        unique_together = ['measurement', 'indicator']
        verbose_name = "Значение измерения"
        verbose_name_plural = "Значения измерений"
    
    def __str__(self):
        return f"{self.indicator.name}: {self.value} {self.indicator.unit}"
    
    def get_color_zone(self):
        """Get color zone for this value"""
        return self.indicator.get_zone_color(self.value)
    
    def get_percentage(self):
        """Get value as percentage of max value"""
        return (self.value / self.indicator.max_value) * 100
