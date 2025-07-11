# Generated by Django 4.2.7 on 2025-06-28 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0002_create_default_schema'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indicator',
            options={'ordering': ['schema__order', 'name']},
        ),
        migrations.AddField(
            model_name='indicator',
            name='schema',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='indicators', to='indicators.schema'),
        ),
        migrations.AlterField(
            model_name='indicator',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='indicator',
            unique_together={('schema', 'name')},
        ),
    ]
