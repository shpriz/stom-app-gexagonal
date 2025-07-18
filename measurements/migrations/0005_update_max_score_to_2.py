# Generated by Django 4.2.7 on 2025-06-28 17:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurements', '0004_alter_measurementvalue_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurementvalue',
            name='value',
            field=models.IntegerField(help_text='Score value (0-2 points)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(2)]),
        ),
    ]
