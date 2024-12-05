from forecast_app.beans.historical_data_bean import HistoricalDataBean
from forecast_app.database_impl.historical_data_database_impl import HistoricalDataDatabaseImpl


class HistoricalDataService:
    @staticmethod
    def get_historical_data(historical_data_id):
        """Retrieve a historical data entry by its ID using the database implementation."""
        return HistoricalDataDatabaseImpl.get_historical_data(historical_data_id)

    @staticmethod
    def add_historical_data(date, day, month, year, customer_age, age_group, customer_gender,
                            country, state, product_category, sub_category, product, order_quantity,
                            unit_cost, unit_price, profit, cost, revenue, is_forecasted, timestamp):
        """Add historical data using the database implementation."""
        historical_data_bean = HistoricalDataBean(
            historical_data_id=None,
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
            timestamp=timestamp
        )
        return HistoricalDataDatabaseImpl.add_historical_data(historical_data_bean)

    @staticmethod
    def get_all_historical_data():
        """Retrieve all historical data entries using the database implementation."""
        return HistoricalDataDatabaseImpl.get_all_historical_data()
