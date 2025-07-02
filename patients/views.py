from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm
from authentication.decorators import (
    active_staff_required, can_edit_patients_required, 
    can_delete_data_required
)


@can_edit_patients_required
def add_patient(request):
    existing_patient = None
    
    if request.method == 'POST':
        form = PatientForm(request.POST, user=request.user)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.doctor = request.user  # Assign current doctor
            patient.save()
            messages.success(request, 'Patient added successfully!')
            return redirect('patient_list')
        else:
            # Check if there's an existing patient in the form validation
            if hasattr(form, 'existing_patient') and form.existing_patient:
                existing_patient = form.existing_patient
    else:
        form = PatientForm(user=request.user)
    
    context = {
        'form': form,
        'existing_patient': existing_patient
    }
    return render(request, 'patients/add_patient.html', context)


@can_edit_patients_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, doctor=request.user)
    
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully!')
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient, user=request.user)
    
    return render(request, 'patients/edit_patient.html', {'form': form, 'patient': patient})


@can_delete_data_required
def delete_patient(request, patient_id):
    """Delete patient and all related data"""
    patient = get_object_or_404(Patient, id=patient_id, doctor=request.user)
    
    # Get statistics about related data that will be deleted
    measurement_count = patient.measurements.count()
    history_count = patient.history.count()
    
    if request.method == 'POST':
        patient_name = patient.full_name
        patient.delete()
        messages.success(request, f'Patient "{patient_name}" and all related data deleted successfully!')
        return redirect('patient_list')
    
    context = {
        'patient': patient,
        'measurement_count': measurement_count,
        'history_count': history_count
    }
    return render(request, 'patients/confirm_delete.html', context)
