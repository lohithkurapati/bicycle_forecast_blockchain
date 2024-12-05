from forecast_app.abstracting.historical_data_abstract import HistoricalDataAbstract
from forecast_app.beans.historical_data_bean import HistoricalDataBean
from forecast_app.models import HistoricalData


class HistoricalDataDatabaseImpl(HistoricalDataAbstract):
    @staticmethod
    def add_historical_data(historical_data_bean: HistoricalDataBean):
        """Add a historical data entry to the database."""
        historical_data = HistoricalData(
            date=historical_data_bean.date,
            day=historical_data_bean.day,
            month=historical_data_bean.month,
            year=historical_data_bean.year,
            customer_age=historical_data_bean.customer_age,
            age_group=historical_data_bean.age_group,
            customer_gender=historical_data_bean.customer_gender,
            country=historical_data_bean.country,
            state=historical_data_bean.state,
            product_category=historical_data_bean.product_category,
            sub_category=historical_data_bean.sub_category,
            product=historical_data_bean.product,
            order_quantity=historical_data_bean.order_quantity,
            unit_cost=historical_data_bean.unit_cost,
            unit_price=historical_data_bean.unit_price,
            profit=historical_data_bean.profit,
            cost=historical_data_bean.cost,
            revenue=historical_data_bean.revenue,
            is_forecasted=historical_data_bean.is_forecasted,
            timestamp=historical_data_bean.timestamp,
            average_forecast=historical_data_bean.average_forecast
        )
        historical_data.save()
        return historical_data.id

    @staticmethod
    def get_historical_data(historical_data_id):
        """Retrieve a historical data entry by ID."""
        try:
            historical_data = HistoricalData.objects.get(pk=historical_data_id)
            return HistoricalDataBean(
                historical_data_id=historical_data.id,
                date=historical_data.date,
                day=historical_data.day,
                month=historical_data.month,
                year=historical_data.year,
                customer_age=historical_data.customer_age,
                age_group=historical_data.age_group,
                customer_gender=historical_data.customer_gender,
                country=historical_data.country,
                state=historical_data.state,
                product_category=historical_data.product_category,
                sub_category=historical_data.sub_category,
                product=historical_data.product,
                order_quantity=historical_data.order_quantity,
                unit_cost=historical_data.unit_cost,
                unit_price=historical_data.unit_price,
                profit=historical_data.profit,
                cost=historical_data.cost,
                revenue=historical_data.revenue,
                is_forecasted=historical_data.is_forecasted,
                timestamp=historical_data.timestamp,
                average_forecast=historical_data.average_forecast
            )
        except HistoricalData.DoesNotExist:
            return None

    @staticmethod
    def get_all_historical_data():
        """Retrieve all historical data entries."""
        historical_data_entries = HistoricalData.objects.all()
        return [
            HistoricalDataBean(
                historical_data_id=hd.id,
                date=hd.date,
                day=hd.day,
                month=hd.month,
                year=hd.year,
                customer_age=hd.customer_age,
                age_group=hd.age_group,
                customer_gender=hd.customer_gender,
                country=hd.country,
                state=hd.state,
                product_category=hd.product_category,
                sub_category=hd.sub_category,
                product=hd.product,
                order_quantity=hd.order_quantity,
                unit_cost=hd.unit_cost,
                unit_price=hd.unit_price,
                profit=hd.profit,
                cost=hd.cost,
                revenue=hd.revenue,
                is_forecasted=hd.is_forecasted,
                timestamp=hd.timestamp,
                average_forecast=hd.average_forecast
            )
            for hd in historical_data_entries
        ]
