from django.urls import path
from . import views

urlpatterns = [
    # Schema management routes
    path('', views.schema_list, name='schema_list'),
    path('add/', views.add_schema, name='add_schema'),
    path('edit/<int:schema_id>/', views.edit_schema, name='edit_schema'),
    path('delete/<int:schema_id>/', views.delete_schema, name='delete_schema'),
]