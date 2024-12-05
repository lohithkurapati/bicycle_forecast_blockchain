from django.db import models
from django.db.models import Avg, Count
from collections import Counter


class AverageForecast(models.Model):
    """
    Saves to the database an average of the forecast details and a key to link each related historical and forecasted data.
    """

    # Name and Path of the Forecast Plot
    total_forecast_plot_path = models.CharField(max_length=255, blank=True, null=True)
    total_forecast_name = models.CharField(max_length=255, blank=True, null=True)
    total_forecast_accuracy = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Date and Time Information
    date = models.DateField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()

    # Customer Information
    customer_age = models.IntegerField(blank=True, null=True)
    age_group = models.CharField(max_length=50, blank=True, null=True)
    customer_gender = models.CharField(max_length=10, blank=True, null=True)

    # Location Information
    country = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)

    # Product Information
    product_category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)
    product = models.CharField(max_length=100, blank=True, null=True)

    # Sales and Financial Data
    order_quantity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    profit = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Forecast Metadata
    is_forecasted = models.BooleanField(blank=True, null=True)
    contract_reference_id = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Average Forecast {self.date} - {self.product} - {self.country}"


class HistoricalData(models.Model):
    """
    Saves to the database the historical data used to generate the forecast.
    """

    # Fields similar to AverageForecast
    date = models.DateField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()

    customer_age = models.IntegerField()
    age_group = models.CharField(max_length=50)
    customer_gender = models.CharField(max_length=10)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    product_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    product = models.CharField(max_length=100)

    order_quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    revenue = models.DecimalField(max_digits=12, decimal_places=2)

    is_forecasted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Link to AverageForecast
    average_forecast = models.ForeignKey('AverageForecast', on_delete=models.CASCADE, blank=True, null=True, related_name='historical_data')

    def __str__(self):
        return f"Historical Data {self.date} - {self.product} - {self.country}"


class Forecast(models.Model):
    """
    Saves to the database the forecasted data.
    """

    # Fields similar to HistoricalData
    date = models.DateField()
    day = models.IntegerField()
    month = models.IntegerField()
    year = models.IntegerField()

    customer_age = models.IntegerField()
    age_group = models.CharField(max_length=50)
    customer_gender = models.CharField(max_length=10)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    product_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    product = models.CharField(max_length=100)

    order_quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    profit = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    revenue = models.DecimalField(max_digits=12, decimal_places=2)

    is_forecasted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Link to AverageForecast
    average_forecast = models.ForeignKey('AverageForecast', on_delete=models.CASCADE, blank=True, null=True, related_name='forecast_data')

    def __str__(self):
        return f"Forecast {self.date} - {self.product} - {self.country}"
