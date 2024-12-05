class ForecastBean:
    def __init__(self, forecast_id, forecast_plot_path, forecast_accuracy, forecast_name, date, day, month, year, customer_age, age_group, customer_gender,
                 country, state, product_category, sub_category, product, order_quantity, unit_cost,
                 unit_price, profit, cost, revenue, is_forecasted, contract_reference_id, timestamp, average_forecast=None):
        self.forecast_id = forecast_id
        self.forecast_plot_path = forecast_plot_path
        self.forecast_accuracy = forecast_accuracy
        self.forecast_name = forecast_name
        self.date = date
        self.day = day
        self.month = month
        self.year = year
        self.customer_age = customer_age
        self.age_group = age_group
        self.customer_gender = customer_gender
        self.country = country
        self.state = state
        self.product_category = product_category
        self.sub_category = sub_category
        self.product = product
        self.order_quantity = order_quantity
        self.unit_cost = unit_cost
        self.unit_price = unit_price
        self.profit = profit
        self.cost = cost
        self.revenue = revenue
        self.is_forecasted = is_forecasted
        self.contract_reference_id = contract_reference_id
        self.timestamp = timestamp,
        self.average_forecast = average_forecast


class AverageForecastBean:
    def __init__(self, average_forecast_id, total_forecast_plot_path, total_forecast_name,
                 total_forecast_accuracy, date, day, month, year, customer_age, age_group, customer_gender, country,
                 state, product_category, sub_category, product, order_quantity, unit_cost, unit_price, profit, cost,
                 revenue, contract_reference_id, timestamp):
        self.average_forecast_id = average_forecast_id
        self.total_forecast_plot_path = total_forecast_plot_path
        self.total_forecast_name = total_forecast_name
        self.total_forecast_accuracy = total_forecast_accuracy
        self.date = date
        self.day = day
        self.month = month
        self.year = year
        self.customer_age = customer_age
        self.age_group = age_group
        self.customer_gender = customer_gender
        self.country = country
        self.state = state
        self.product_category = product_category
        self.sub_category = sub_category
        self.product = product
        self.order_quantity = order_quantity
        self.unit_cost = unit_cost
        self.unit_price = unit_price
        self.profit = profit
        self.cost = cost
        self.revenue = revenue
        self.contract_reference_id = contract_reference_id
        self.timestamp = timestamp
