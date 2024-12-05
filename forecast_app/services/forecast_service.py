from forecast_app.beans.forecast_bean import ForecastBean
from forecast_app.database_impl.forecast_database_impl import ForecastDatabaseImpl
from forecast_app.models import AverageForecast


class ForecastService:
    @staticmethod
    def get_forecast(forecast_id):
        """Retrieve a forecast by its ID using the database implementation."""
        return ForecastDatabaseImpl.get_forecast(forecast_id)

    @staticmethod
    def save_forecast(forecast_plot_path, forecast_accuracy, forecast_name,date, day, month, year, customer_age, age_group, customer_gender, country, state,
                      product_category, sub_category, product, order_quantity, unit_cost, unit_price,
                      profit, cost, revenue, is_forecasted, contract_reference_id, timestamp):
        """Save a new forecast entry using the database implementation."""
        forecast_bean = ForecastBean(
            forecast_id=None,
            forecast_plot_path=forecast_plot_path,
            forecast_accuracy=forecast_accuracy,
            forecast_name=forecast_name,
            date=date,
            day=day,
            month=month,
            year=year,
            customer_age=customer_age,
            age_group=age_group,
            customer_gender=customer_gender,
            country=country,
            state=state,
            product_category=product_category,
            sub_category=sub_category,
            product=product,
            order_quantity=order_quantity,
            unit_cost=unit_cost,
            unit_price=unit_price,
            profit=profit,
            cost=cost,
            revenue=revenue,
            is_forecasted=is_forecasted,
            contract_reference_id=contract_reference_id,
            timestamp=timestamp
        )
        return ForecastDatabaseImpl.save_forecast(forecast_bean)


    @staticmethod
    def get_all_forecasts():
        """Retrieve all forecasts using the database implementation, ordered by forecast and historical."""
        return ForecastDatabaseImpl.get_all_forecasts()
