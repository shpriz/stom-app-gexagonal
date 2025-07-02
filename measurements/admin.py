from django.contrib import admin
from .models import Measurement, MeasurementValue


class MeasurementValueInline(admin.TabularInline):
    model = MeasurementValue
    extra = 6
    max_num = 6


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ['patient', 'measurement_date', 'show_in_chart', 'created_at']
    list_filter = ['show_in_chart', 'measurement_date', 'created_at']
    search_fields = ['patient__first_name', 'patient__last_name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MeasurementValueInline]
    
    fieldsets = (
        ('Measurement Info', {
            'fields': ('patient', 'measurement_date', 'show_in_chart')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(MeasurementValue)
class MeasurementValueAdmin(admin.ModelAdmin):
    list_display = ['measurement', 'indicator', 'value', 'get_color_zone', 'get_percentage']
    list_filter = ['indicator', 'measurement__measurement_date']
    search_fields = ['measurement__patient__first_name', 'measurement__patient__last_name', 'indicator__name']
    
    def get_color_zone(self, obj):
        return obj.get_color_zone()
    get_color_zone.short_description = 'Color Zone'
    
    def get_percentage(self, obj):
        return f"{obj.get_percentage():.1f}%"
    get_percentage.short_description = 'Percentage'
