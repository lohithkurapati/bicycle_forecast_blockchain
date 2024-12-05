from forecast_app.beans.historical_data_bean import HistoricalDataBean


class HistoricalDataAbstract:
    @staticmethod
    def add_historical_data(historical_data_bean: HistoricalDataBean):
        """Add a historical data entry to the database."""
        raise NotImplementedError

    @staticmethod
    def get_historical_data(historical_data_id):
        """Retrieve a historical data entry by its ID."""
        raise NotImplementedError

    @staticmethod
    def get_all_historical_data():
        """Retrieve all historical data entries."""
        raise NotImplementedError