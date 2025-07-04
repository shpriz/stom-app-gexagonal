from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Schema(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    order = models.PositiveIntegerField(default=1, help_text="Порядок отображения (1=первая, 2=вторая, и т.д.)", verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлена")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Схема"
        verbose_name_plural = "Схемы"
    
    def __str__(self):
        return f"Схема {self.order}: {self.name}"


class Indicator(models.Model):
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name='indicators', null=True, blank=True, verbose_name="Схема")
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    min_value = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Минимальное значение")
    max_value = models.FloatField(validators=[MinValueValidator(0)], verbose_name="Максимальное значение")
    
    # Color zone thresholds (as percentages of max_value)
    green_threshold = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=80,
        help_text="Green zone starts at this percentage of max value"
    )
    yellow_threshold = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=60,
        help_text="Yellow zone starts at this percentage of max value"
    )
    
    unit = models.CharField(max_length=20, blank=True, help_text="Unit of measurement (e.g., mm, %, points)")
    
    # Automatic scoring thresholds
    score_0_max = models.FloatField(
        null=True, blank=True,
        help_text="Maximum value for 0 points (e.g., 28 for OHIP, 19 for smoking)"
    )
    score_1_max = models.FloatField(
        null=True, blank=True,
        help_text="Maximum value for 1 point (e.g., 42 for OHIP, leave blank for open-ended)"
    )
    score_2_max = models.FloatField(
        null=True, blank=True,
        help_text="Maximum value for 2 points (optional, for 3+ point scales)"
    )
    
    # Special handling for zero/empty values
    zero_value_score = models.IntegerField(
        default=0,
        choices=[(0, '0 points'), (1, '1 point'), (2, '2 points')],
        help_text="Score when value is 0 or empty (e.g., 0 points for 'Does not smoke')"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    
    class Meta:
        ordering = ['schema__order', 'name']
        unique_together = ['schema', 'name']
        verbose_name = "Индикатор"
        verbose_name_plural = "Индикаторы"
    
    def __str__(self):
        return f"{self.schema.name}: {self.name} ({self.min_value}-{self.max_value} {self.unit})"
    
    def get_zone_color(self, value):
        """Return color zone for a given value"""
        if value is None:
            return 'gray'
        
        percentage = (value / self.max_value) * 100
        
        if percentage >= self.green_threshold:
            return 'green'
        elif percentage >= self.yellow_threshold:
            return 'yellow'
        else:
            return 'red'
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.min_value >= self.max_value:
            raise ValidationError('Min value must be less than max value')
        if self.green_threshold <= self.yellow_threshold:
            raise ValidationError('Green threshold must be greater than yellow threshold')
    
    def calculate_score(self, raw_value):
        """Calculate score based on scoring ranges"""
        if raw_value is None:
            return 0
            
        # Get scoring ranges for this indicator
        ranges = self.scoring_ranges.all().order_by('score')
        
        for scoring_range in ranges:
            if scoring_range.is_value_in_range(raw_value):
                return scoring_range.score
        
        # If no range matches, return 0
        return 0


class ScoringRange(models.Model):
    """Определяет диапазоны оценок для индикаторов"""
    indicator = models.ForeignKey(Indicator, on_delete=models.CASCADE, related_name='scoring_ranges', verbose_name="Индикатор")
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(2)], verbose_name="Балл")
    
    # Range definition
    min_value = models.FloatField(null=True, blank=True, help_text="Минимальное значение (включительно)", verbose_name="Минимальное значение")
    max_value = models.FloatField(null=True, blank=True, help_text="Максимальное значение (включительно)", verbose_name="Максимальное значение")
    step = models.FloatField(default=1.0, help_text="Шаг между минимальным и максимальным значениями (по умолчанию: 1)", verbose_name="Шаг")
    
    # Special cases
    is_greater_than_or_equal = models.BooleanField(default=False, help_text="≥ минимального значения (игнорирует максимальное значение)", verbose_name="Больше или равно")
    is_less_than = models.BooleanField(default=False, help_text="< максимального значения (игнорирует минимальное значение)", verbose_name="Меньше чем")
    exact_value = models.FloatField(null=True, blank=True, help_text="Точное совпадение значения (для конкретных значений как 0, 1, 2)", verbose_name="Точное значение")
    
    description = models.CharField(max_length=100, help_text="Описание как '0-28', '≥20', 'Не курит'", verbose_name="Описание")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    
    class Meta:
        ordering = ['indicator', 'score']
        unique_together = ['indicator', 'score']
        verbose_name = "Диапазон оценок"
        verbose_name_plural = "Диапазоны оценок"
    
    def __str__(self):
        return f"{self.indicator.name}: {self.description} = {self.score} points"
    
    def is_value_in_range(self, value):
        """Check if a value falls within this scoring range"""
        if value is None:
            return False
        
        # Exact value match (for backward compatibility)
        if self.exact_value is not None:
            return abs(value - self.exact_value) < 0.001  # Handle floating point precision
        
        # Exact value through min/max being equal
        if (self.min_value is not None and self.max_value is not None and 
            abs(self.min_value - self.max_value) < 0.001):
            return abs(value - self.min_value) < 0.001
        
        # Special cases
        if self.is_greater_than_or_equal and self.min_value is not None:
            return value >= self.min_value
            
        if self.is_less_than and self.max_value is not None:
            return value < self.max_value
        
        # Normal range check
        min_ok = self.min_value is None or value >= self.min_value
        max_ok = self.max_value is None or value <= self.max_value
        
        return min_ok and max_ok
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Count how many range methods are being used
        methods_used = 0
        if self.exact_value is not None:
            methods_used += 1
        if self.min_value is not None and self.max_value is not None:
            methods_used += 1
        if self.is_greater_than_or_equal and self.min_value is not None:
            methods_used += 1
        if self.is_less_than and self.max_value is not None:
            methods_used += 1
        
        # Validate that at least one range definition method is used
        if methods_used == 0:
            raise ValidationError('Must specify a range: set min_value and max_value, or use special conditions')
        
        # Validate range logic
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                raise ValidationError('Min value must be less than or equal to max value')
            
            # Validate step
            if self.step <= 0:
                raise ValidationError('Step must be positive')
        
        # Validate step is only used with min/max ranges
        if self.step != 1.0 and (self.min_value is None or self.max_value is None):
            raise ValidationError('Step can only be used with min/max value ranges')


class RecommendationTemplate(models.Model):
    """Шаблон медицинских рекомендаций на основе баллов схемы"""
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, related_name='recommendation_templates', verbose_name="Схема")
    
    # Risk level definition
    risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Низкий риск'),
        ('moderate', 'Умеренный риск'), 
        ('high', 'Высокий риск')
    ], verbose_name="Уровень риска")
    
    # Score range for this recommendation
    min_score = models.IntegerField(help_text="Минимальный общий балл для этого уровня риска", verbose_name="Минимальный балл")
    max_score = models.IntegerField(help_text="Максимальный общий балл для этого уровня риска", verbose_name="Максимальный балл")
    
    # Recommendation content
    title = models.CharField(max_length=200, help_text="Заголовок оценки риска", verbose_name="Заголовок")
    description = models.TextField(help_text="Описание уровня риска", verbose_name="Описание")
    recommendations = models.TextField(help_text="Подробные медицинские рекомендации", verbose_name="Рекомендации")
    
    # DEPRECATED: Keep for backward compatibility but will be replaced with IndicatorRecommendation
    indicator_recommendations = models.JSONField(
        default=dict,
        help_text="УСТАРЕЛО: Используйте отдельные рекомендации по индикаторам",
        verbose_name="Рекомендации по индикаторам (устарело)",
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        ordering = ['schema', 'min_score']
        unique_together = ['schema', 'risk_level']
        verbose_name = "Шаблон рекомендаций"
        verbose_name_plural = "Шаблоны рекомендаций"
    
    def __str__(self):
        return f"{self.schema.name}: {self.get_risk_level_display()} ({self.min_score}-{self.max_score} баллов)"
    
    def is_score_in_range(self, total_score):
        """Check if a total score falls within this recommendation's range"""
        return self.min_score <= total_score <= self.max_score

    def get_indicator_recommendations(self):
        """Get indicator-specific recommendations, preferring new model over JSON"""
        # Get from new model first
        indicator_recs = {}
        for rec in self.indicator_recommendations_new.all():
            indicator_recs[rec.indicator.name] = rec.recommendation_text
        
        # Fall back to JSON field if no new recommendations exist
        if not indicator_recs and self.indicator_recommendations:
            indicator_recs = self.indicator_recommendations
        
        return indicator_recs


class IndicatorRecommendation(models.Model):
    """Рекомендация по конкретному индикатору для уровня риска"""
    recommendation_template = models.ForeignKey(
        RecommendationTemplate, 
        on_delete=models.CASCADE, 
        related_name='indicator_recommendations_new',
        verbose_name="Шаблон рекомендаций"
    )
    indicator = models.ForeignKey(
        Indicator, 
        on_delete=models.CASCADE,
        verbose_name="Индикатор"
    )
    
    # Recommendation for different score levels
    recommendation_text = models.TextField(
        help_text="Рекомендация для этого индикатора при данном уровне риска",
        verbose_name="Текст рекомендации"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")
    
    class Meta:
        ordering = ['recommendation_template', 'indicator__name']
        unique_together = ['recommendation_template', 'indicator']
        verbose_name = "Рекомендация по индикатору"
        verbose_name_plural = "Рекомендации по индикаторам"
    
    def __str__(self):
        return f"{self.recommendation_template.get_risk_level_display()} - {self.indicator.name}"
