# utils.py

import calendar

# Define month options using the calendar module
month_options = [{'label': month, 'value': month} for month in calendar.month_name if month]
month_order = list(calendar.month_name)[1:]  # Skip empty string at index 0
