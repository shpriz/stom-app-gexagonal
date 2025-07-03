#!/usr/bin/env python
import os
import django
import sys
from datetime import date
import random

# Setup Django environment
sys.path.append('/home/shpriz/projects/zykova/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dental_office.settings')
django.setup()

from django.contrib.auth.models import User
from patients.models import Patient

# Get the first doctor user
try:
    doctor = User.objects.filter(is_staff=True).first()
    if not doctor:
        doctor = User.objects.first()
    
    if not doctor:
        print("No users found in database. Please create a user first.")
        exit(1)
        
    print(f"Adding patients for doctor: {doctor.username}")
    
except Exception as e:
    print(f"Error finding doctor: {e}")
    exit(1)

# Test patients data (mix of men and women)
patients_data = [
    # Мужчины
    {
        'history_of_illness': '2024001',
        'first_name': 'Александр',
        'last_name': 'Петров',
        'patronymic': 'Сергеевич',
        'date_of_birth': date(1975, 3, 15)
    },
    {
        'history_of_illness': '2024002', 
        'first_name': 'Михаил',
        'last_name': 'Иванов',
        'patronymic': 'Владимирович',
        'date_of_birth': date(1962, 8, 22)
    },
    {
        'history_of_illness': '2024003',
        'first_name': 'Дмитрий',
        'last_name': 'Смирнов',
        'patronymic': 'Алексеевич',
        'date_of_birth': date(1983, 11, 7)
    },
    {
        'history_of_illness': '2024004',
        'first_name': 'Андрей',
        'last_name': 'Козлов',
        'patronymic': 'Николаевич',
        'date_of_birth': date(1957, 4, 12)
    },
    {
        'history_of_illness': '2024005',
        'first_name': 'Сергей',
        'last_name': 'Новikov',
        'patronymic': 'Игоревич',
        'date_of_birth': date(1989, 1, 28)
    },
    
    # Женщины  
    {
        'history_of_illness': '2024006',
        'first_name': 'Елена',
        'last_name': 'Васильева',
        'patronymic': 'Михайловна',
        'date_of_birth': date(1971, 6, 19)
    },
    {
        'history_of_illness': '2024007',
        'first_name': 'Анна',
        'last_name': 'Морозова',
        'patronymic': 'Дмитриевна',
        'date_of_birth': date(1965, 9, 3)
    },
    {
        'history_of_illness': '2024008',
        'first_name': 'Ольга',
        'last_name': 'Волкова',
        'patronymic': 'Александровна',
        'date_of_birth': date(1978, 12, 14)
    },
    {
        'history_of_illness': '2024009',
        'first_name': 'Татьяна',
        'last_name': 'Соколова',
        'patronymic': 'Сергеевна',
        'date_of_birth': date(1942, 5, 8)
    },
    {
        'history_of_illness': '2024010',
        'first_name': 'Марина',
        'last_name': 'Лебедева',
        'patronymic': 'Викторовна',
        'date_of_birth': date(1986, 10, 25)
    }
]

# Add patients to database
created_count = 0
skipped_count = 0

for patient_data in patients_data:
    try:
        # Check if patient already exists
        if Patient.objects.filter(
            history_of_illness=patient_data['history_of_illness'],
            doctor=doctor
        ).exists():
            print(f"Patient {patient_data['history_of_illness']} already exists, skipping...")
            skipped_count += 1
            continue
            
        # Create new patient
        patient = Patient.objects.create(
            doctor=doctor,
            history_of_illness=patient_data['history_of_illness'],
            first_name=patient_data['first_name'],
            last_name=patient_data['last_name'],
            patronymic=patient_data['patronymic'],
            date_of_birth=patient_data['date_of_birth'],
            phone_number='0'  # Default value
        )
        
        print(f"✅ Created patient: {patient.full_name} (№{patient.history_of_illness})")
        created_count += 1
        
    except Exception as e:
        print(f"❌ Error creating patient {patient_data['history_of_illness']}: {e}")

print(f"\n📊 Summary:")
print(f"Created: {created_count} patients")
print(f"Skipped: {skipped_count} patients")
print(f"Total: {created_count + skipped_count} patients processed")