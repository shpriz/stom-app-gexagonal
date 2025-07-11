# Generated by Django 4.2.7 on 2025-06-28 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0005_add_scoring_ranges'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoringrange',
            name='step',
            field=models.FloatField(default=1.0, help_text='Step between min and max values (default: 1)'),
        ),
        migrations.AlterField(
            model_name='scoringrange',
            name='exact_value',
            field=models.FloatField(blank=True, help_text='Exact value match (for specific values like 0, 1, 2)', null=True),
        ),
        migrations.AlterField(
            model_name='scoringrange',
            name='max_value',
            field=models.FloatField(blank=True, help_text='Maximum value (inclusive)', null=True),
        ),
        migrations.AlterField(
            model_name='scoringrange',
            name='min_value',
            field=models.FloatField(blank=True, help_text='Minimum value (inclusive)', null=True),
        ),
    ]
