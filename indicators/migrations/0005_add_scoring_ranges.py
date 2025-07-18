# Generated by Django 4.2.7 on 2025-06-28 07:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0004_assign_default_schema'),
    ]

    operations = [
        migrations.AddField(
            model_name='indicator',
            name='score_0_max',
            field=models.FloatField(blank=True, help_text='Maximum value for 0 points (e.g., 28 for OHIP, 19 for smoking)', null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='score_1_max',
            field=models.FloatField(blank=True, help_text='Maximum value for 1 point (e.g., 42 for OHIP, leave blank for open-ended)', null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='score_2_max',
            field=models.FloatField(blank=True, help_text='Maximum value for 2 points (optional, for 3+ point scales)', null=True),
        ),
        migrations.AddField(
            model_name='indicator',
            name='zero_value_score',
            field=models.IntegerField(choices=[(0, '0 points'), (1, '1 point'), (2, '2 points'), (3, '3 points')], default=0, help_text="Score when value is 0 or empty (e.g., 0 points for 'Does not smoke')"),
        ),
        migrations.CreateModel(
            name='ScoringRange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(3)])),
                ('min_value', models.FloatField(blank=True, help_text="Minimum value (inclusive). Leave blank for 'less than max_value'", null=True)),
                ('max_value', models.FloatField(blank=True, help_text="Maximum value (inclusive). Leave blank for 'greater than or equal to min_value'", null=True)),
                ('is_greater_than_or_equal', models.BooleanField(default=False, help_text='≥ min_value (ignores max_value)')),
                ('is_less_than', models.BooleanField(default=False, help_text='< max_value (ignores min_value)')),
                ('exact_value', models.FloatField(blank=True, help_text='Exact value match (overrides range)', null=True)),
                ('description', models.CharField(help_text="Description like '0-28', '≥20', 'Does not smoke'", max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scoring_ranges', to='indicators.indicator')),
            ],
            options={
                'ordering': ['indicator', 'score'],
                'unique_together': {('indicator', 'score')},
            },
        ),
    ]
