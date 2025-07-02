from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_patient, name='add_patient'),
    path('edit/<int:patient_id>/', views.edit_patient, name='edit_patient'),
    path('delete/<int:patient_id>/', views.delete_patient, name='delete_patient'),
]