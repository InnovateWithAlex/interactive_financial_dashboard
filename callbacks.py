# callbacks.py

from dash.dependencies import Input, Output, State
from app import app
from dash import html, dcc
import dash_bootstrap_components as dbc
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
from layouts import create_layout

# Callback to render the content based on selected tab
@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-investments':
        # Placeholder for Investments tab content
        return html.Div([
            html.H3('Investments Section'),
            # Include your existing investment components here
        ])
    elif tab == 'tab-budgeting':
        # Budgeting tab content
        return html.Div([
            html.H3('Budgeting Section'),
            # Budget Input Form
            html.Div([
                html.H4('Enter Budget Data'),
                html.Label('Category:'),
                dcc.Input(id='budget-category', type='text', placeholder='Category'),
                html.Label('Budgeted Amount:'),
                dcc.Input(id='budget-amount', type='number', placeholder='Amount'),
                html.Button('Add Budget', id='add-budget-button', n_clicks=0)
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
                html.Button('Add Actual', id='add-actual-button', n_clicks=0)
            ]),
            html.Hr(),
            # Visualization
            html.Div([
                dcc.Graph(id='budget-vs-actual-chart')
            ])
        ])

# Callback to handle adding budget data and updating the chart
@app.callback(
    Output('budget-vs-actual-chart', 'figure'),
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
    # Handle adding budget data
    if budget_clicks and budget_clicks > 0 and budget_category and budget_amount is not None:
        new_budget = {'Category': budget_category, 'Budgeted Amount': budget_amount, 'Time Period': 'Monthly'}
        save_budget_data(new_budget)

    # Handle adding actual expenditure data
    if actual_clicks and actual_clicks > 0 and actuals_category and actuals_amount is not None and actuals_date:
        new_actual = {'Category': actuals_category, 'Actual Amount': actuals_amount, 'Date': actuals_date}
        save_actuals_data(new_actual)

    # Load data and perform calculations
    budget_data = load_budget_data()
    actuals_data = load_actuals_data()
    merged_data = calculate_budget_vs_actual(budget_data, actuals_data)

    # Create visualization
    fig = create_budget_vs_actual_chart(merged_data)

    return fig
