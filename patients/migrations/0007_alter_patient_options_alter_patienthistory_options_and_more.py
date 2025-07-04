# Generated by Django 4.2.7 on 2025-07-03 19:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patients', '0006_patient_doctor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ['last_name', 'first_name'], 'verbose_name': 'Пациент', 'verbose_name_plural': 'Пациенты'},
        ),
        migrations.AlterModelOptions(
            name='patienthistory',
            options={'ordering': ['-changed_at'], 'verbose_name': 'История имени пациента', 'verbose_name_plural': 'История имен пациентов'},
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.TextField(blank=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Создан'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(help_text='Врач, ответственный за этого пациента', on_delete=django.db.models.deletion.CASCADE, related_name='patients', to=settings.AUTH_USER_MODEL, verbose_name='Врач'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='history_of_illness',
            field=models.CharField(help_text='Номер истории болезни (уникальный идентификатор)', max_length=10, unique=True, verbose_name='Номер истории болезни'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(default='0', max_length=20, validators=[django.core.validators.RegexValidator(message='Номер телефона может содержать цифры, пробелы, +, -, ( )', regex='^[\\d\\s\\+\\-\\(\\)]{1,20}$')], verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлен'),
        ),
        migrations.AlterField(
            model_name='patienthistory',
            name='changed_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Изменено'),
        ),
        migrations.AlterField(
            model_name='patienthistory',
            name='changed_by',
            field=models.CharField(blank=True, max_length=100, verbose_name='Изменено пользователем'),
        ),
        migrations.AlterField(
            model_name='patienthistory',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='patienthistory',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='patienthistory',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='patients.patient', verbose_name='Пациент'),
        ),
        migrations.AlterField(
            model_name='patienthistory',
            name='patronymic',
            field=models.CharField(blank=True, max_length=100, verbose_name='Отчество'),
        ),
    ]
