from django.contrib import admin
from django import forms
from .models import Schema, Indicator, ScoringRange, RecommendationTemplate, IndicatorRecommendation


class ScoringRangeForm(forms.ModelForm):
    class Meta:
        model = ScoringRange
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set default values
        if not self.instance.pk:  # New instance
            self.fields['step'].initial = 1.0
            self.fields['min_value'].initial = 0
            self.fields['max_value'].initial = 10
        
        # Add helpful attributes
        self.fields['step'].widget.attrs.update({
            'step': '0.1',
            'min': '0.1',
            'style': 'width: 80px;'
        })
        self.fields['min_value'].widget.attrs.update({
            'step': '0.1',
            'style': 'width: 80px;'
        })
        self.fields['max_value'].widget.attrs.update({
            'step': '0.1', 
            'style': 'width: 80px;'
        })


class ScoringRangeInline(admin.TabularInline):
    model = ScoringRange
    form = ScoringRangeForm
    extra = 1
    fields = ['score', 'description', 'min_value', 'max_value', 'step', 'is_greater_than_or_equal', 'is_less_than']
    verbose_name = "Scoring Range"
    verbose_name_plural = "Scoring Ranges"


@admin.register(ScoringRange)
class ScoringRangeAdmin(admin.ModelAdmin):
    form = ScoringRangeForm
    list_display = ['indicator', 'score', 'description', 'get_range_display']
    list_filter = ['indicator__schema', 'indicator', 'score']
    search_fields = ['indicator__name', 'description']
    ordering = ['indicator', 'score']
    
    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('indicator', 'score', 'description'),
            'description': 'Enter the score (0-2 points) and a description like "0-28 (low risk)"'
        }),
        ('📊 Range Definition', {
            'fields': ('min_value', 'max_value', 'step'),
            'description': '''
            <strong>Examples:</strong><br/>
            • OHIP 0-28 points: min_value=0, max_value=28, step=1<br/>
            • Age 18-65 years: min_value=18, max_value=65, step=1<br/>
            • Height 1.5-2.0m: min_value=1.5, max_value=2.0, step=0.1<br/>
            • For exact values like "0 cigarettes": min_value=0, max_value=0, step=1
            '''
        }),
        ('⚡ Special Conditions (for open-ended ranges)', {
            'fields': ('is_greater_than_or_equal', 'is_less_than'),
            'description': '''
            <strong>Examples:</strong><br/>
            • "≥20 cigarettes": is_greater_than_or_equal=True, min_value=20<br/>
            • "<5 years": is_less_than=True, max_value=5<br/>
            • "≥2 diseases": is_greater_than_or_equal=True, min_value=2
            '''
        }),
    )
    
    def get_range_display(self, obj):
        """Show human-readable range"""
        if obj.exact_value is not None:
            return f"= {obj.exact_value}"
        elif obj.is_greater_than_or_equal and obj.min_value is not None:
            return f"≥ {obj.min_value}"
        elif obj.is_less_than and obj.max_value is not None:
            return f"< {obj.max_value}"
        elif obj.min_value is not None and obj.max_value is not None:
            # Check if it's an exact value (min = max)
            if abs(obj.min_value - obj.max_value) < 0.001:
                return f"= {obj.min_value}"
            else:
                step_display = f" (step: {obj.step})" if obj.step != 1.0 else ""
                return f"{obj.min_value} - {obj.max_value}{step_display}"
        elif obj.min_value is not None:
            return f"≥ {obj.min_value}"
        elif obj.max_value is not None:
            return f"≤ {obj.max_value}"
        else:
            return "Invalid range"
    
    get_range_display.short_description = 'Range'


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    class Meta:
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"


@admin.register(Indicator)
class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'schema', 'min_value', 'max_value', 'unit', 'green_threshold', 'yellow_threshold', 'is_active']
    list_filter = ['schema', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    inlines = [ScoringRangeInline]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('schema', 'name', 'description', 'unit', 'is_active')
        }),
        ('Value Range', {
            'fields': ('min_value', 'max_value')
        }),
        ('Color Zones (%)', {
            'fields': ('green_threshold', 'yellow_threshold'),
            'description': 'Thresholds as percentage of max value'
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


class IndicatorRecommendationInline(admin.TabularInline):
    model = IndicatorRecommendation
    extra = 0
    fields = ['indicator', 'recommendation_text']
    verbose_name = "Рекомендация по индикатору"
    verbose_name_plural = "Рекомендации по индикаторам"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Filter indicators by schema"""
        if db_field.name == "indicator":
            # Get the recommendation template object from the URL
            try:
                template_id = request.resolver_match.kwargs.get('object_id')
                if template_id:
                    template = RecommendationTemplate.objects.get(id=template_id)
                    kwargs["queryset"] = Indicator.objects.filter(schema=template.schema, is_active=True)
                else:
                    kwargs["queryset"] = Indicator.objects.filter(is_active=True)
            except (RecommendationTemplate.DoesNotExist, ValueError):
                kwargs["queryset"] = Indicator.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(RecommendationTemplate)
class RecommendationTemplateAdmin(admin.ModelAdmin):
    list_display = ['schema', 'get_risk_level_display', 'min_score', 'max_score', 'title']
    list_filter = ['schema', 'risk_level']
    search_fields = ['title', 'description']
    ordering = ['schema', 'min_score']
    inlines = [IndicatorRecommendationInline]
    
    fieldsets = (
        ('🏥 Схема и уровень риска', {
            'fields': ('schema', 'risk_level', 'min_score', 'max_score'),
            'description': 'Выберите схему обследования и определите диапазон баллов для уровня риска'
        }),
        ('📝 Содержание рекомендации', {
            'fields': ('title', 'description', 'recommendations'),
            'description': '''
            <strong>Заполните медицинские рекомендации:</strong><br/>
            • <strong>Заголовок:</strong> Краткое описание уровня риска<br/>
            • <strong>Описание:</strong> Диапазон баллов и объяснение<br/>
            • <strong>Рекомендации:</strong> Подробные медицинские инструкции
            '''
        }),
    )
    
    def get_risk_level_display(self, obj):
        return obj.get_risk_level_display()
    get_risk_level_display.short_description = 'Уровень риска'
    
    def save_model(self, request, obj, form, change):
        """Save the recommendation template"""
        super().save_model(request, obj, form, change)


@admin.register(IndicatorRecommendation)
class IndicatorRecommendationAdmin(admin.ModelAdmin):
    list_display = ['recommendation_template', 'indicator', 'get_short_recommendation']
    list_filter = ['recommendation_template__schema', 'recommendation_template__risk_level', 'indicator']
    search_fields = ['indicator__name', 'recommendation_text']
    ordering = ['recommendation_template', 'indicator__name']
    
    fieldsets = (
        ('Базовая информация', {
            'fields': ('recommendation_template', 'indicator'),
            'description': 'Выберите шаблон рекомендации и индикатор'
        }),
        ('Рекомендация', {
            'fields': ('recommendation_text',),
            'description': 'Введите конкретную рекомендацию для этого индикатора'
        }),
    )
    
    def get_short_recommendation(self, obj):
        """Show truncated recommendation text"""
        text = obj.recommendation_text
        return text[:100] + "..." if len(text) > 100 else text
    get_short_recommendation.short_description = 'Рекомендация'
