# Generated by Django 4.2.7 on 2025-06-27 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_patient_history_of_illness'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='history_of_illness',
            field=models.CharField(blank=True, help_text='Medical history and previous illnesses', max_length=10),
        ),
    ]
