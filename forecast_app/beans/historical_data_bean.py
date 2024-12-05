class HistoricalDataBean:
    def __init__(self, historical_data_id, date, day, month, year, customer_age, age_group, customer_gender,
                 country, state, product_category, sub_category, product, order_quantity, unit_cost, unit_price,
                 profit, cost, revenue, is_forecasted, timestamp, average_forecast=None):
        self.historical_data_id = historical_data_id
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
        self.timestamp = timestamp
        self.average_forecast = average_forecast
