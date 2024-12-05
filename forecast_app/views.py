import json
import os
from datetime import datetime

import pandas as pd
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from forecast_app.blockchain.contract_compile import compile_contract
from forecast_app.blockchain.contract_init import init_contract
from forecast_app.blockchain.contract_interaction import store_forecast
from forecast_app.blockchain.contract_setup import deploy_contract
from forecast_app.maf.accuracy import calculate_accuracy
from forecast_app.maf.data_limiter import limit_data_range
from forecast_app.maf.forecasting import generate_forecast
from forecast_app.maf.plotting import plot_forecast
from forecast_app.models import HistoricalData, Forecast, AverageForecast


def index(request):
    """
    Render the main forecast dashboard.
    """
    forecasts = AverageForecast.objects.all()
    return render(request, "index.html", {"forecasts": forecasts})


def validate_date_range(request):
    if request.method == "POST":
        source_start_date = request.POST.get("start_source")
        source_end_date = request.POST.get("end_source")
        forecast_start_date = request.POST.get("start_forecast")
        forecast_end_date = request.POST.get("end_forecast")

        try:
            # Parse dates
            source_start_date = datetime.strptime(source_start_date, "%Y-%m-%d")
            source_end_date = datetime.strptime(source_end_date, "%Y-%m-%d")
            forecast_start_date = datetime.strptime(forecast_start_date, "%Y-%m-%d")
            forecast_end_date = datetime.strptime(forecast_end_date, "%Y-%m-%d")

            # Validate historical data date range
            if (source_end_date - source_start_date).days > 180:
                return JsonResponse({"error": "Historical range must not exceed 6 months."}, status=400)

            if source_end_date > datetime.now():
                return JsonResponse({"error": "End date must not be in the future."}, status=400)

            if source_start_date > source_end_date:
                return JsonResponse({"error": "Start date must be before end date."}, status=400)

            # Validate forecast date range
            if (forecast_end_date - forecast_start_date).days > 90:
                return JsonResponse({"error": "Forecast range must not exceed 3 months."}, status=400)

            if forecast_start_date != source_end_date:
                return JsonResponse({"error": "Forecast start date must match historical end date."}, status=400)

            if forecast_start_date > forecast_end_date:
                return JsonResponse({"error": "Forecast start date must be before end date."}, status=400)

            # Load and process historical data
            hist_data = pd.read_csv(os.path.join(settings.DATA_DIR, 'bike_sales_data.csv'), parse_dates=['Date'])
            hist_data = limit_data_range(hist_data, source_end_date, 2)

            # Generate forecast data
            forecast_data = generate_forecast(hist_data, forecast_start_date, forecast_end_date)

            # Fill NaN values with 0
            forecast_data = forecast_data.fillna(0)

            # Convert relevant columns to integers
            forecast_data['Day'] = forecast_data['Day'].astype(int)
            forecast_data['Year'] = forecast_data['Year'].astype(int)
            forecast_data['Customer_Age'] = forecast_data['Customer_Age'].astype(int)
            forecast_data['Order_Quantity'] = forecast_data['Order_Quantity'].astype(int)
            forecast_data['Unit_Cost'] = forecast_data['Unit_Cost'].astype(int)
            forecast_data['Unit_Price'] = forecast_data['Unit_Price'].astype(int)
            forecast_data['Profit'] = forecast_data['Profit'].astype(int)
            forecast_data['Cost'] = forecast_data['Cost'].astype(int)
            forecast_data['Revenue'] = forecast_data['Revenue'].astype(int)

            # Save to directory for debugging
            forecast_data.to_csv(os.path.join(settings.FORECAST_DIR, 'forecast_data.csv'), index=False)

            # Combine historical and forecast data for plotting
            hist_data['Forecast'] = False
            forecast_data['Forecast'] = True

            # Generate and save plot
            plot_path = os.path.join(settings.FORECAST_PLT_DIR,
                                     f"Forecast_{datetime.now().strftime('%Y%m%d%H%M%S')}.png")
            # plot the forecast
            plot_forecast(forecast_data, plot_path)

            # Save data to database
            avg_forecast_id = save_average_forecast(forecast_data, plot_path)
            save_historical_data(hist_data, avg_forecast_id)
            save_forecast_data(forecast_data, avg_forecast_id)

            # Compile and deploy the contract
            compile_contract()
            deploy_contract()

            # Initialize the contract
            contract_instance, web3 = init_contract()

            # get average forecast data from the database, convert to dictionary and store on the blockchain
            avg_forecast = AverageForecast.objects.get(id=avg_forecast_id)
            avg_forecast_data = avg_forecast.__dict__

            # remove unnecessary fields
            avg_forecast_data.pop('_state')
            avg_forecast_data.pop('id')
            avg_forecast_data.pop('timestamp')
            avg_forecast_data.pop('total_forecast_plot_path')
            avg_forecast_data.pop('total_forecast_name')
            avg_forecast_data.pop('contract_reference_id')
            avg_forecast_data.pop('is_forecasted')

            # convert all decimal fields to int
            avg_forecast_data['total_forecast_accuracy'] = int(avg_forecast_data['total_forecast_accuracy'])
            avg_forecast_data['customer_age'] = int(avg_forecast_data['customer_age'])
            avg_forecast_data['order_quantity'] = int(avg_forecast_data['order_quantity'])
            avg_forecast_data['unit_cost'] = int(avg_forecast_data['unit_cost'])
            avg_forecast_data['unit_price'] = int(avg_forecast_data['unit_price'])
            avg_forecast_data['profit'] = int(avg_forecast_data['profit'])
            avg_forecast_data['cost'] = int(avg_forecast_data['cost'])
            avg_forecast_data['revenue'] = int(avg_forecast_data['revenue'])

            # convert date to string
            avg_forecast_data['date'] = avg_forecast_data['date'].strftime('%Y-%m-%d')

            # store forecast data on the blockchain
            store_forecast(avg_forecast_id, json.dumps(avg_forecast_data), contract_instance, web3)

            # update average_forecast model with contract reference id
            avg_forecast = AverageForecast.objects.get(id=avg_forecast_id)
            avg_forecast.contract_reference_id = contract_instance.address
            avg_forecast.save()

            return JsonResponse({"message": "Data validated and forecast generated successfully."})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def save_historical_data(hist_data, avg_forecast_id):
    HistoricalData.objects.bulk_create([
        HistoricalData(
            date=row['Date'],
            day=row['Date'].day,
            month=row['Date'].month,
            year=row['Date'].year,
            customer_age=row['Customer_Age'] if pd.notna(row['Customer_Age']) else None,
            age_group=row.get('Age_Group', ''),
            customer_gender=row.get('Customer_Gender', ''),
            country=row.get('Country', ''),
            state=row.get('State', ''),
            product_category=row.get('Product_Category', ''),
            sub_category=row.get('Sub_Category', ''),
            product=row.get('Product', ''),
            order_quantity=row['Order_Quantity'],
            unit_cost=row['Unit_Cost'],
            unit_price=row['Unit_Price'],
            profit=row['Profit'],
            cost=row['Cost'],
            revenue=row['Revenue'],
            is_forecasted=False,
            timestamp=datetime.now(),
            average_forecast_id=avg_forecast_id
        ) for _, row in hist_data.iterrows()
    ])


def save_forecast_data(forecast_data, avg_forecast_id):
    Forecast.objects.bulk_create([
        Forecast(
            date=row['Date'],
            day=row['Date'].day,
            month=row['Date'].month,
            year=row['Date'].year,
            customer_age=row['Customer_Age'] if pd.notna(row['Customer_Age']) else None,
            age_group=row.get('Age_Group', ''),
            customer_gender=row.get('Customer_Gender', ''),
            country=row.get('Country', ''),
            state=row.get('State', ''),
            product_category=row.get('Product_Category', ''),
            sub_category=row.get('Sub_Category', ''),
            product=row.get('Product', ''),
            order_quantity=row['Order_Quantity'],
            unit_cost=row['Unit_Cost'],
            unit_price=row['Unit_Price'],
            profit=row['Profit'],
            cost=row['Cost'],
            revenue=row['Revenue'],
            is_forecasted=True,
            timestamp=datetime.now(),
            average_forecast_id=avg_forecast_id
        ) for _, row in forecast_data.iterrows()
    ])


def save_average_forecast(forecast_data, plot_path):
    avg_forecast = AverageForecast(
        total_forecast_plot_path=plot_path,
        total_forecast_name=f"Forecast_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        total_forecast_accuracy=calculate_accuracy(
            forecast_data['Order_Quantity'],
            [forecast_data['Order_Quantity']] * 3  # Mock additional forecasts
        ),
        date=forecast_data['Date'].iloc[0],
        day=forecast_data['Date'].iloc[0].day,
        month=forecast_data['Date'].iloc[0].month,
        year=forecast_data['Date'].iloc[0].year,
        customer_age=forecast_data['Customer_Age'].mean(),
        age_group=forecast_data['Age_Group'].mode()[0],
        customer_gender=forecast_data['Customer_Gender'].mode()[0],
        country=forecast_data['Country'].mode()[0],
        state=forecast_data['State'].mode()[0],
        product_category=forecast_data['Product_Category'].mode()[0],
        sub_category=forecast_data['Sub_Category'].mode()[0],
        product=forecast_data['Product'].mode()[0],
        order_quantity=forecast_data['Order_Quantity'].mean(),
        unit_cost=forecast_data['Unit_Cost'].mean(),
        unit_price=forecast_data['Unit_Price'].mean(),
        profit=forecast_data['Profit'].mean(),
        cost=forecast_data['Cost'].mean(),
        revenue=forecast_data['Revenue'].mean(),
        is_forecasted=True,
        timestamp=datetime.now()
    )
    avg_forecast.save()
    return avg_forecast.id


def render_forecast_table(request, average_forecast_id=None):
    avg_forecast = None
    forecast_data = []
    historical_data = []

    if average_forecast_id:
        avg_forecast = get_object_or_404(AverageForecast, id=average_forecast_id)
        forecast_data = Forecast.objects.filter(average_forecast=avg_forecast)
        historical_data = HistoricalData.objects.filter(average_forecast=avg_forecast)

    context = {
        "forecasts": AverageForecast.objects.all(),  # For sidebar
        "avg_forecast": avg_forecast,  # Selected average forecast
        "forecast_data": forecast_data,
        "historical_data": historical_data,
    }
    return render(request, "index.html", context)
