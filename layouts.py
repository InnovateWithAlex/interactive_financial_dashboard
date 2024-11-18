# layouts.py

from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return html.Div([
        html.H1("Empire Builder Financial Dashboard"),

        # Tabs for navigation
        dcc.Tabs(id='tabs', value='tab-investments', children=[
            dcc.Tab(label='Investments', value='tab-investments'),
            dcc.Tab(label='Budgeting', value='tab-budgeting'),
        ]),

        html.Div(id='tabs-content')
    ])
