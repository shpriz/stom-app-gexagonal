from django.contrib import admin
from .models import Patient, PatientHistory


class PatientHistoryInline(admin.TabularInline):
    model = PatientHistory
    extra = 0
    readonly_fields = ['changed_at']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'date_of_birth', 'phone_number', 'created_at']
    list_filter = ['created_at', 'date_of_birth']
    search_fields = ['first_name', 'last_name', 'patronymic', 'phone_number', 'email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PatientHistoryInline]
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'patronymic', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email', 'address')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(PatientHistory)
class PatientHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'first_name', 'last_name', 'patronymic', 'changed_at']
    list_filter = ['changed_at']
    readonly_fields = ['changed_at']
