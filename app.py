# app.py

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc  # For Bootstrap components

# Import our modules
from data.data_storage import (
    load_budget_data,
    save_budget_data,
    load_actuals_data,
    save_actuals_data
)
from calculations.budget_calculations import (
    calculate_budget_vs_actual,
    calculate_total_variance
)
from visualizations.budget_visualizations import create_budget_vs_actual_chart

# Initialize Dash app with Bootstrap styles
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout with budgeting features
app.layout = html.Div([
    html.H1("Empire Builder Financial Dashboard - Budgeting"),

    # Budget Input Form
    html.Div([
        html.H4('Enter Budget Data'),
        html.Label('Category:'),
        dcc.Input(id='budget-category', type='text', placeholder='Category'),
        html.Label('Budgeted Amount:'),
        dcc.Input(id='budget-amount', type='number', placeholder='Amount'),
        html.Button('Add Budget', id='add-budget-button', n_clicks=0),
        html.Div(id='budget-message', style={'color': 'red'})  # Placeholder for messages
    ]),
    html.Hr(),
    # Actuals Input Form
    html.Div([
        html.H4('Enter Actual Expenditure Data'),
        html.Label('Category:'),
        dcc.Input(id='actuals-category', type='text', placeholder='Category'),
        html.Label('Actual Amount:'),
        dcc.Input(id='actuals-amount', type='number', placeholder='Amount'),
        html.Label('Date:'),
        dcc.DatePickerSingle(id='actuals-date'),
        html.Button('Add Actual', id='add-actual-button', n_clicks=0),
        html.Div(id='actuals-message', style={'color': 'red'})  # Placeholder for messages
    ]),
    html.Hr(),
    # Visualization
    html.Div([
        dcc.Graph(id='budget-vs-actual-chart')
    ])
])

# Callback to handle adding budget data and updating the chart
@app.callback(
    [Output('budget-vs-actual-chart', 'figure'),
     Output('budget-message', 'children'),
     Output('actuals-message', 'children'),
     Output('budget-category', 'value'),
     Output('budget-amount', 'value'),
     Output('actuals-category', 'value'),
     Output('actuals-amount', 'value'),
     Output('actuals-date', 'date')],
    [Input('add-budget-button', 'n_clicks'),
     Input('add-actual-button', 'n_clicks')],
    [State('budget-category', 'value'),
     State('budget-amount', 'value'),
     State('actuals-category', 'value'),
     State('actuals-amount', 'value'),
     State('actuals-date', 'date')]
)
def update_budget_actual_chart(budget_clicks, actual_clicks,
                               budget_category, budget_amount,
                               actuals_category, actuals_amount, actuals_date):
    budget_message = ''
    actuals_message = ''

    # Handle adding budget data
    if budget_clicks and budget_clicks > 0:
        if not budget_category or budget_amount is None:
            budget_message = 'Please enter a valid category and budgeted amount.'
        else:
            try:
                new_budget = {'Category': budget_category, 'Budgeted Amount': budget_amount, 'Time Period': 'Monthly'}
                save_budget_data(new_budget)
                budget_message = f'Budget data saved for category: {budget_category}.'
                # Clear input fields
                budget_category = None
                budget_amount = None
            except Exception as e:
                budget_message = f"Error saving budget data: {e}"

    # Handle adding actual expenditure data
    if actual_clicks and actual_clicks > 0:
        if not actuals_category or actuals_amount is None or actuals_date is None:
            actuals_message = 'Please enter a valid category, amount, and date.'
        else:
            try:
                new_actual = {'Category': actuals_category, 'Actual Amount': actuals_amount, 'Date': actuals_date}
                save_actuals_data(new_actual)
                actuals_message = f'Actual expenditure data saved for category: {actuals_category}.'
                # Clear input fields
                actuals_category = None
                actuals_amount = None
                actuals_date = None
            except Exception as e:
                actuals_message = f"Error saving actual expenditure data: {e}"

    # Load data and perform calculations
    try:
        budget_data = load_budget_data()
        actuals_data = load_actuals_data()
        merged_data = calculate_budget_vs_actual(budget_data, actuals_data)

        # Create visualization
        fig = create_budget_vs_actual_chart(merged_data)
    except Exception as e:
        print(f"Error updating chart: {e}")
        # Create an empty figure with an error message
        fig = go.Figure()
        fig.update_layout(
            title='Error generating chart',
            xaxis_title='Category',
            yaxis_title='Amount'
        )

    return fig, budget_message, actuals_message, budget_category, budget_amount, actuals_category, actuals_amount, actuals_date

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)