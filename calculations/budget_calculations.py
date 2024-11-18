# calculations/budget_calculations.py

import pandas as pd

def calculate_budget_vs_actual(budget_data, actuals_data):
    """
    Calculate variances between budgeted amounts and actual spending per category.
    """
    # Merge data on 'Category'
    merged_data = pd.merge(budget_data, actuals_data, on='Category', how='outer')
    merged_data = merged_data.fillna(0)
    merged_data['Variance'] = merged_data['Budgeted Amount'] - merged_data['Actual Amount']
    return merged_data

def calculate_total_variance(merged_data):
    """
    Calculate total budgeted, actual, and variance amounts.
    """
    total_budgeted = merged_data['Budgeted Amount'].sum()
    total_actual = merged_data['Actual Amount'].sum()
    total_variance = total_budgeted - total_actual
    return total_budgeted, total_actual, total_variance
