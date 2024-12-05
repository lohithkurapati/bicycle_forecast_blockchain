from django.contrib import admin
from .models import AverageForecast, HistoricalData, Forecast

@admin.register(AverageForecast)
class AverageForecastAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'product', 'country', 'total_forecast_name', 'total_forecast_accuracy', 'is_forecasted', 'timestamp'
    )
    list_filter = ('date', 'product', 'country', 'is_forecasted')
    search_fields = ('product', 'country', 'total_forecast_name')
    ordering = ('-timestamp',)

@admin.register(HistoricalData)
class HistoricalDataAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'product', 'country', 'order_quantity', 'profit', 'revenue', 'is_forecasted', 'timestamp'
    )
    list_filter = ('date', 'product', 'country', 'is_forecasted')
    search_fields = ('product', 'country')
    ordering = ('-timestamp',)

@admin.register(Forecast)
class ForecastAdmin(admin.ModelAdmin):
    list_display = (
        'date', 'product', 'country', 'order_quantity', 'profit', 'revenue', 'is_forecasted', 'timestamp'
    )
    list_filter = ('date', 'product', 'country', 'is_forecasted')
    search_fields = ('product', 'country')
    ordering = ('-timestamp',)
