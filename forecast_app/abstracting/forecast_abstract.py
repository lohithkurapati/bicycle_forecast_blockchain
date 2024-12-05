from forecast_app.beans.forecast_bean import ForecastBean, AverageForecastBean


class ForecastAbstract:
    @staticmethod
    def get_forecast(forecast_id):
        """Retrieve a forecast entry by its ID."""
        raise NotImplementedError

    @staticmethod
    def save_forecast(forecast_bean: ForecastBean):
        """Save a new forecast entry."""
        raise NotImplementedError

    @staticmethod
    def calculate_and_save_average_forecast(average_forecast_bean: AverageForecastBean):
        """Calculate and save an average forecast entry."""
        raise NotImplementedError

    @staticmethod
    def get_all_forecasts():
        """Retrieve all forecast entries, ordered with forecasts at the top followed by historical data."""
        raise NotImplementedError

    @staticmethod
    def get_average_forecast(average_forecast_id):
        """Retrieve an average forecast entry by its ID."""
        raise NotImplementedError

    @staticmethod
    def get_all_average_forecasts():
        """Retrieve all average forecast entries."""
        raise NotImplementedError
