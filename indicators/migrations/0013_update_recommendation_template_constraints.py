# Generated by Django 4.2.7 on 2025-07-04 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0012_alter_recommendationtemplate_indicator_recommendations_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='recommendationtemplate',
            unique_together={('schema', 'risk_level', 'min_score', 'max_score')},
        ),
    ]
