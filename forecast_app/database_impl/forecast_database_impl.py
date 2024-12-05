from forecast_app.abstracting.forecast_abstract import ForecastAbstract
from forecast_app.beans.forecast_bean import ForecastBean
from forecast_app.models import Forecast, AverageForecast


class ForecastDatabaseImpl(ForecastAbstract):
    @staticmethod
    def get_forecast(forecast_id):
        """Retrieve a forecast by ID."""
        try:
            forecast = Forecast.objects.get(pk=forecast_id)
            return ForecastBean(
                forecast_id=forecast.id,
                forecast_plot_path=forecast.forecast_plot_path,
                forecast_accuracy=forecast.forecast_accuracy,
                forecast_name=forecast.forecast_name,
                date=forecast.date,
                day=forecast.day,
                month=forecast.month,
                year=forecast.year,
                customer_age=forecast.customer_age,
                age_group=forecast.age_group,
                customer_gender=forecast.customer_gender,
                country=forecast.country,
                state=forecast.state,
                product_category=forecast.product_category,
                sub_category=forecast.sub_category,
                product=forecast.product,
                order_quantity=forecast.order_quantity,
                unit_cost=forecast.unit_cost,
                unit_price=forecast.unit_price,
                profit=forecast.profit,
                cost=forecast.cost,
                revenue=forecast.revenue,
                is_forecasted=forecast.is_forecasted,
                contract_reference_id=forecast.contract_reference_id,
                timestamp=forecast.timestamp,
                average_forecast=forecast.average_forecast
            )
        except Forecast.DoesNotExist:
            return None

    @staticmethod
    def save_forecast(forecast_bean: ForecastBean):
        """Save a new forecast entry."""
        forecast = Forecast(
            forecast_plot_path=forecast_bean.forecast_plot_path,
            forecast_accuracy=forecast_bean.forecast_accuracy,
            forecast_name=forecast_bean.forecast_name,
            date=forecast_bean.date,
            day=forecast_bean.day,
            month=forecast_bean.month,
            year=forecast_bean.year,
            customer_age=forecast_bean.customer_age,
            age_group=forecast_bean.age_group,
            customer_gender=forecast_bean.customer_gender,
            country=forecast_bean.country,
            state=forecast_bean.state,
            product_category=forecast_bean.product_category,
            sub_category=forecast_bean.sub_category,
            product=forecast_bean.product,
            order_quantity=forecast_bean.order_quantity,
            unit_cost=forecast_bean.unit_cost,
            unit_price=forecast_bean.unit_price,
            profit=forecast_bean.profit,
            cost=forecast_bean.cost,
            revenue=forecast_bean.revenue,
            is_forecasted=forecast_bean.is_forecasted,
            contract_reference_id=forecast_bean.contract_reference_id,
            timestamp=forecast_bean.timestamp,
            average_forecast=forecast_bean.average_forecast
        )
        forecast.save()
        return forecast.id


    @staticmethod
    def get_all_forecasts():
        """Retrieve all forecasts, ordered by forecasted (future) data first, then historical data."""
        forecasts = Forecast.objects.order_by('-is_forecasted', 'date')
        return [
            ForecastBean(
                forecast_id=f.id,
                forecast_plot_path=f.forecast_plot_path,
                forecast_accuracy=f.forecast_accuracy,
                forecast_name=f.forecast_name,
                date=f.date,
                day=f.day,
                month=f.month,
                year=f.year,
                customer_age=f.customer_age,
                age_group=f.age_group,
                customer_gender=f.customer_gender,
                country=f.country,
                state=f.state,
                product_category=f.product_category,
                sub_category=f.sub_category,
                product=f.product,
                order_quantity=f.order_quantity,
                unit_cost=f.unit_cost,
                unit_price=f.unit_price,
                profit=f.profit,
                cost=f.cost,
                revenue=f.revenue,
                is_forecasted=f.is_forecasted,
                contract_reference_id=f.contract_reference_id,
                timestamp=f.timestamp,
                average_forecast=f.average_forecast
            )
            for f in forecasts
        ]
