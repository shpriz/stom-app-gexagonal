from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'measurements', views.MeasurementViewSet)

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('chart/<int:patient_id>/', views.radar_chart_view, name='radar_chart'),
    path('measurement/add/<int:patient_id>/', views.add_measurement, name='add_measurement'),
    path('measurement/edit/<int:measurement_id>/', views.edit_measurement, name='edit_measurement'),
    path('measurement/delete/<int:measurement_id>/', views.delete_measurement, name='delete_measurement'),
    path('api/', include(router.urls)),
]