# maf/accuracy.py
import numpy as np

def calculate_accuracy(initial_forecast, additional_forecasts):
    """Calculates the forecast accuracy based on the mean of additional forecasts."""
    average_forecast = np.mean(additional_forecasts, axis=0)
    accuracy = 100 - np.mean(np.abs((initial_forecast - average_forecast) / average_forecast)) * 100
    return round(accuracy, 2)
