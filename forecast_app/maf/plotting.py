import matplotlib.pyplot as plt
import pandas as pd

def plot_forecast(data, filename, downsample_factor=10, smoothing_window=7):
    """
    Plots the forecasted and historical data with reduced noise.
    :param data: DataFrame containing the forecast and historical data.
    :param filename: Path to save the plot.
    :param downsample_factor: Integer factor to downsample the data (e.g., plot every nth point).
    :param smoothing_window: Window size for smoothing using a moving average.
    """
    plt.figure(figsize=(10, 6))

    # Ensure data is sorted by date
    data = data.sort_values(by='Date')

    # Separate forecasted and historical data
    historical_data = data[data['Forecast'] == False]
    forecasted_data = data[data['Forecast'] == True]

    # Apply smoothing (moving average) to reduce noise
    historical_data['Smoothed_Order_Quantity'] = historical_data['Order_Quantity'].rolling(window=smoothing_window).mean()
    forecasted_data['Smoothed_Order_Quantity'] = forecasted_data['Order_Quantity'].rolling(window=smoothing_window).mean()

    # Downsample the data to reduce plotted points (plot every nth point)
    historical_data = historical_data.iloc[::downsample_factor]
    forecasted_data = forecasted_data.iloc[::downsample_factor]

    # Plot the smoothed and downsampled historical data
    plt.plot(
        historical_data['Date'],
        historical_data['Smoothed_Order_Quantity'],
        color='blue'
    )

    # Plot the smoothed and downsampled forecasted data
    plt.plot(
        forecasted_data['Date'],
        forecasted_data['Smoothed_Order_Quantity'],
        label='Forecast (Smoothed)',
        color='orange',
    )

    # Add labels, legend, and title
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Order Quantity')
    plt.title('Bicycle Sales Forecast (Smoothed)')

    # Save the plot
    plt.savefig(filename)
    plt.close()
