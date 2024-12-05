from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('validate_date_range/', views.validate_date_range, name='validate_date_range'),
    path('api/forecasts/', views.index, name='sidebar_forecast_list'),
    path('forecast/<int:average_forecast_id>/', views.render_forecast_table, name='render_forecast_table'),
]
