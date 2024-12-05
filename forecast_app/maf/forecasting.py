import pandas as pd

from forecast_app.maf.config import HISTORICAL_LIMIT_YEARS, FORECAST_LIMIT_MONTHS
from forecast_app.maf.data_limiter import limit_data_range


def calculate_moving_average(data, window=3):
    """Calculates moving average forecast based on historical data."""
    data.loc[:, 'Forecast'] = data['Order_Quantity'].rolling(window=window).mean()
    return data.dropna()

def generate_forecast(data, start_date, end_date):
    """Generates forecasted data within the specified range."""
    # Limit historical data to the latest 2 years
    historical_data = limit_data_range(data, end_date, HISTORICAL_LIMIT_YEARS)

    # Calculate the moving average
    forecast_data = calculate_moving_average(historical_data)

    # Create forecast for the next 6 months
    last_order_quantity = forecast_data['Order_Quantity'].iloc[-1]
    forecast_dates = pd.date_range(start=start_date, periods=FORECAST_LIMIT_MONTHS, freq='MS')
    forecast_values = [last_order_quantity] * FORECAST_LIMIT_MONTHS
    forecast_df = pd.DataFrame({'Date': forecast_dates, 'Order_Quantity': forecast_values, 'Forecast': True})

    return pd.concat([forecast_data, forecast_df], ignore_index=True)