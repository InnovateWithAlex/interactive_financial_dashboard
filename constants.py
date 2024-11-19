# constants.py

from utils import month_options
from dash import dash_table

# Define columns for Income and Expenses tables
income_columns = [
    {'name': 'Month', 'id': 'Month', 'presentation': 'dropdown', 'editable': True},
    {'name': 'Source', 'id': 'Source', 'type': 'text', 'editable': True},
    {'name': 'Budgeted Amount', 'id': 'Budgeted Amount', 'type': 'numeric', 'editable': True},
    {'name': 'Actual Amount', 'id': 'Actual Amount', 'type': 'numeric', 'editable': True},
    {'name': 'Variance', 'id': 'Variance', 'type': 'numeric', 'editable': False}
]

expenses_columns = [
    {'name': 'Month', 'id': 'Month', 'presentation': 'dropdown', 'editable': True},
    {'name': 'Category', 'id': 'Category', 'type': 'text', 'editable': True},
    {'name': 'Budgeted Amount', 'id': 'Budgeted Amount', 'type': 'numeric', 'editable': True},
    {'name': 'Actual Amount', 'id': 'Actual Amount', 'type': 'numeric', 'editable': True},
    {'name': 'Variance', 'id': 'Variance', 'type': 'numeric', 'editable': False}
]

# Initialize data with a blank row
income_data = [{'Month': '', 'Source': '', 'Budgeted Amount': '', 'Actual Amount': '', 'Variance': ''}]
expenses_data = [{'Month': '', 'Category': '', 'Budgeted Amount': '', 'Actual Amount': '', 'Variance': ''}]
