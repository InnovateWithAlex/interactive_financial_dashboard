import dash
from dash import Dash, html, dcc, Input, Output, State, dash_table
import pandas as pd
import calendar

app = Dash(__name__)

# Define month options
month_options = [{'label': month, 'value': month} for month in calendar.month_name if month]

# Define columns
columns = [
    {'name': 'Month', 'id': 'Month', 'type': 'text', 'presentation': 'dropdown', 'editable': True},
    {'name': 'Value', 'id': 'Value', 'type': 'numeric', 'editable': True}
]

# Initial data
data = [{'Month': '', 'Value': ''}]

# Layout
app.layout = html.Div([
    dash_table.DataTable(
        id='test-table',
        columns=columns,
        data=data,
        editable=True,
        dropdown={
            'Month': {
                'options': month_options
            }
        }
    ),
    html.Button('Add Row', id='add-row', n_clicks=0)
])

# Callback to add a new row
@app.callback(
    Output('test-table', 'data'),
    Input('add-row', 'n_clicks'),
    State('test-table', 'data'),
    State('test-table', 'columns'),
    prevent_initial_call=True
)
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
