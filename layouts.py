# layouts.py

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from constants import income_columns, expenses_columns, income_data, expenses_data
from utils import month_options

# Define the app layout
app_layout = dbc.Container([
    dbc.Row(
        dbc.Col(html.H1("Empire Builder Financial Dashboard - Budgeting", className="text-center text-primary mb-4"))
    ),
    
    # Income Section
    dbc.Row([
        dbc.Col(html.H2('Income'), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='income-table',
                columns=income_columns,
                data=income_data,
                editable=True,
                row_deletable=True,
                dropdown={
                    'Month': {
                        'options': month_options
                    }
                },
                style_table={'margin-bottom': '20px'}
            ),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Button('Add Income Row', id='add-income-row', n_clicks=0, color='primary'),
            width=12
        )
    ]),
    
    # Expenses Section
    dbc.Row([
        dbc.Col(html.H2('Expenses'), width=12)
    ]),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='expenses-table',
                columns=expenses_columns,
                data=expenses_data,
                editable=True,
                row_deletable=True,
                dropdown={
                    'Month': {
                        'options': month_options
                    }
                },
                style_table={'margin-bottom': '20px'}
            ),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Button('Add Expense Row', id='add-expenses-row', n_clicks=0, color='primary'),
            width=12
        )
    ]),
    
    # Save and Clear Buttons
    dbc.Row([
        dbc.Col(
            dbc.Button('Save Data', id='save-button', n_clicks=0, color='success', className='mr-2'),
            width='auto'
        ),
        dbc.Col(
            dbc.Button('Clear Data', id='clear-button', n_clicks=0, color='danger'),
            width='auto'
        )
    ], justify='start', className='mt-3'),
    
    # Filters
    dbc.Row([
        dbc.Col(html.H3('Filters'), width=12)
    ], className='mt-4'),
    dbc.Row([
        dbc.Col([
            html.Label('Select Income Sources:'),
            dcc.Dropdown(
                id='income-source-filter',
                options=[],  # Options will be populated dynamically
                multi=True,
                placeholder="Select income sources"
            )
        ], width=6),
        dbc.Col([
            html.Label('Select Expense Categories:'),
            dcc.Dropdown(
                id='expense-category-filter',
                options=[],  # Options will be populated dynamically
                multi=True,
                placeholder="Select expense categories"
            )
        ], width=6)
    ]),
    
    # Financial Metrics
    dbc.Row([
        dbc.Col(html.H3('Financial Metrics'), width=12)
    ], className='mt-4'),
    dbc.Row([
        dbc.Col(
            html.Div(id='financial-metrics'),
            width=12
        )
    ]),
    
    # Visualizations
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='budget-vs-actual-chart'),
            width=12
        )
    ], className='mt-4'),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='cumulative-cash-flow-chart'),
            width=12
        )
    ], className='mt-4'),
], fluid=True)
