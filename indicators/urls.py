from django.urls import path
from . import views

urlpatterns = [
    # Indicator management (both /indicators/ and /indicator/ routes)
    path('', views.indicator_list, name='indicator_list'),
    path('add/', views.add_indicator, name='add_indicator'),
    path('edit/<int:indicator_id>/', views.edit_indicator, name='edit_indicator'),
    path('delete/<int:indicator_id>/', views.delete_indicator, name='delete_indicator'),
    path('<int:indicator_id>/scoring-ranges/', views.manage_scoring_ranges, name='manage_scoring_ranges'),
]