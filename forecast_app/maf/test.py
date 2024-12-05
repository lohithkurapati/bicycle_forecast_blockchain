# maf/test.py
import pandas as pd

from forecast_app.maf.config import FORECAST_LIMIT_MONTHS
from forecasting import generate_forecast
from plotting import plot_forecast
from accuracy import calculate_accuracy


def run_test():
    # Load sample data
    data = pd.read_csv("../../data/bike_sales_data.csv", parse_dates=['Date'])

    # Define the forecast range (3 months)
    start_date = data['Date'].max() + pd.DateOffset(months=1)
    end_date = start_date + pd.DateOffset(months=3)

    # Generate forecast
    forecast_data = generate_forecast(data, start_date, end_date)

    # Save forecast data to CSV
    forecast_data.to_csv("../../static/forecast_predictions/test_prediction.csv", index=False)

    # Plot forecast and save image
    plot_forecast(forecast_data, "../../static/forecast_plots/test_forecast.png")

    # Calculate and print accuracy
    initial_forecast = forecast_data['Order_Quantity'][-FORECAST_LIMIT_MONTHS:].values
    additional_forecasts = [initial_forecast] * 3  # Simulating additional forecasts for testing
    accuracy = calculate_accuracy(initial_forecast, additional_forecasts)
    print(f"Forecast accuracy: {accuracy}%")


if __name__ == "__main__":
    run_test()
