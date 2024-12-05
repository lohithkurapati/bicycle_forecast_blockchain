# maf/data_limiter.py
from datetime import timedelta

def limit_data_range(data, end_date, years_limit):
    """Limits data to the specified range in years."""
    start_date = end_date - timedelta(days=years_limit * 365)
    return data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
