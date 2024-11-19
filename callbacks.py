# callbacks.py

from dash.dependencies import Input, Output, State
from dash import callback_context
import pandas as pd
from app_instance import app
from dash import html
import plotly.graph_objs as go
from utils import month_order
from dash.exceptions import PreventUpdate

# Callback to update income table
@app.callback(
    Output('income-table', 'data'),
    [Input('add-income-row', 'n_clicks'),
     Input('income-table', 'data_timestamp'),
     Input('clear-button', 'n_clicks')],
    [State('income-table', 'data'),
     State('income-table', 'columns')],
    prevent_initial_call=True
)
def update_income_table(add_row_clicks, data_timestamp, clear_clicks, rows, columns):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'clear-button':
        # Clear data
        return []

    elif triggered_id == 'add-income-row':
        if rows is None:
            rows = []
        # Initialize new row with empty values
        rows.append({c['id']: '' for c in columns})
        return rows

    elif triggered_id == 'income-table':
        # Update Variance without altering cell properties
        updated_rows = []
        for row in rows:
            new_row = row.copy()
            budgeted = float(new_row.get('Budgeted Amount') or 0)
            actual = float(new_row.get('Actual Amount') or 0)
            new_row['Variance'] = actual - budgeted
            updated_rows.append(new_row)
        return updated_rows

    else:
        raise PreventUpdate

# Callback to update expenses table
@app.callback(
    Output('expenses-table', 'data'),
    [Input('add-expenses-row', 'n_clicks'),
     Input('expenses-table', 'data_timestamp'),
     Input('clear-button', 'n_clicks')],
    [State('expenses-table', 'data'),
     State('expenses-table', 'columns')],
    prevent_initial_call=True
)
def update_expenses_table(add_row_clicks, data_timestamp, clear_clicks, rows, columns):
    ctx = callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'clear-button':
        # Clear data
        return []

    elif triggered_id == 'add-expenses-row':
        if rows is None:
            rows = []
        # Initialize new row with empty values
        rows.append({c['id']: '' for c in columns})
        return rows

    elif triggered_id == 'expenses-table':
        # Update Variance without altering cell properties
        updated_rows = []
        for row in rows:
            new_row = row.copy()
            budgeted = float(new_row.get('Budgeted Amount') or 0)
            actual = float(new_row.get('Actual Amount') or 0)
            new_row['Variance'] = budgeted - actual  # For expenses
            updated_rows.append(new_row)
        return updated_rows

    else:
        raise PreventUpdate

# Callback to update filter options
@app.callback(
    [Output('income-source-filter', 'options'),
     Output('expense-category-filter', 'options')],
    [Input('income-table', 'data'),
     Input('expenses-table', 'data')]
)
def update_filter_options(income_data, expenses_data):
    income_df = pd.DataFrame(income_data)
    expenses_df = pd.DataFrame(expenses_data)

    income_sources = income_df['Source'].dropna().unique().tolist()
    expense_categories = expenses_df['Category'].dropna().unique().tolist()

    income_source_options = [{'label': src, 'value': src} for src in income_sources]
    expense_category_options = [{'label': cat, 'value': cat} for cat in expense_categories]

    return income_source_options, expense_category_options

# Callback to update the main chart based on filters
@app.callback(
    Output('budget-vs-actual-chart', 'figure'),
    [Input('income-table', 'data'),
     Input('expenses-table', 'data'),
     Input('income-source-filter', 'value'),
     Input('expense-category-filter', 'value')]
)
def update_chart(income_data, expenses_data, selected_sources, selected_categories):
    # Convert data to DataFrames
    income_df = pd.DataFrame(income_data)
    expenses_df = pd.DataFrame(expenses_data)

    # Filter income data based on selected sources
    if selected_sources:
        income_df = income_df[income_df['Source'].isin(selected_sources)]
    # Filter expenses data based on selected categories
    if selected_categories:
        expenses_df = expenses_df[expenses_df['Category'].isin(selected_categories)]

    # Ensure 'Month' column exists
    for df in [income_df, expenses_df]:
        if 'Month' not in df.columns:
            df['Month'] = ''

    # Ensure numeric columns are of correct type
    for df in [income_df, expenses_df]:
        for col in ['Budgeted Amount', 'Actual Amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Group data by Month and sum
    income_summary = income_df.groupby('Month')[['Budgeted Amount', 'Actual Amount']].sum().reset_index()
    expenses_summary = expenses_df.groupby('Month')[['Budgeted Amount', 'Actual Amount']].sum().reset_index()

    # Merge income and expenses data
    summary_df = pd.merge(
        income_summary,
        expenses_summary,
        on='Month',
        how='outer',
        suffixes=('_Income', '_Expenses')
    ).fillna(0)

    # Sort the months according to calendar order
    summary_df['Month'] = pd.Categorical(summary_df['Month'], categories=month_order, ordered=True)
    summary_df = summary_df.sort_values('Month')

    # Create Figure with grouped bars
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=summary_df['Month'],
        y=summary_df['Budgeted Amount_Income'],
        name='Budgeted Income',
        marker_color='green'
    ))

    fig.add_trace(go.Bar(
        x=summary_df['Month'],
        y=summary_df['Actual Amount_Income'],
        name='Actual Income',
        marker_color='lightgreen'
    ))

    fig.add_trace(go.Bar(
        x=summary_df['Month'],
        y=-summary_df['Budgeted Amount_Expenses'],
        name='Budgeted Expenses',
        marker_color='red'
    ))

    fig.add_trace(go.Bar(
        x=summary_df['Month'],
        y=-summary_df['Actual Amount_Expenses'],
        name='Actual Expenses',
        marker_color='salmon'
    ))

    fig.update_layout(
        title='Budgeted vs Actual Income and Expenses',
        xaxis_title='Month',
        yaxis_title='Amount',
        barmode='group',
        template='plotly_white',
        legend_title='Legend',
    )

    # Adjust y-axis to display negative expenses correctly
    fig.update_yaxes(tickprefix="$", showgrid=True)

    return fig

# Callback to update the cumulative cash flow chart
@app.callback(
    Output('cumulative-cash-flow-chart', 'figure'),
    [Input('income-table', 'data'),
     Input('expenses-table', 'data')]
)
def update_cumulative_cash_flow_chart(income_data, expenses_data):
    # Convert data to DataFrames
    income_df = pd.DataFrame(income_data)
    expenses_df = pd.DataFrame(expenses_data)

    # Ensure 'Month' column exists
    for df in [income_df, expenses_df]:
        if 'Month' not in df.columns:
            df['Month'] = ''

    # Ensure numeric columns are of correct type
    for df in [income_df, expenses_df]:
        for col in ['Actual Amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Group data by Month and sum Actual Amounts
    income_summary = income_df.groupby('Month')['Actual Amount'].sum().reset_index()
    expenses_summary = expenses_df.groupby('Month')['Actual Amount'].sum().reset_index()

    # Merge income and expenses data
    summary_df = pd.merge(
        income_summary,
        expenses_summary,
        on='Month',
        how='outer',
        suffixes=('_Income', '_Expenses')
    ).fillna(0)

    # Calculate Net Income and Cumulative Net Income
    summary_df['Net Income'] = summary_df['Actual Amount_Income'] - summary_df['Actual Amount_Expenses']

    # Sort the months according to calendar order
    summary_df['Month'] = pd.Categorical(summary_df['Month'], categories=month_order, ordered=True)
    summary_df = summary_df.sort_values('Month')

    # Calculate cumulative net income
    summary_df['Cumulative Net Income'] = summary_df['Net Income'].cumsum()

    # Create Figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=summary_df['Month'],
        y=summary_df['Cumulative Net Income'],
        name='Cumulative Net Income',
        mode='lines+markers',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        title='Cumulative Net Income Over Time',
        xaxis_title='Month',
        yaxis_title='Cumulative Net Income',
        template='plotly_white',
        legend_title='Legend',
    )

    fig.update_yaxes(tickprefix="$", showgrid=True)

    return fig

# Callback to update financial metrics
@app.callback(
    Output('financial-metrics', 'children'),
    [Input('income-table', 'data'),
     Input('expenses-table', 'data')]
)
def update_financial_metrics(income_data, expenses_data):
    # Convert data to DataFrames
    income_df = pd.DataFrame(income_data)
    expenses_df = pd.DataFrame(expenses_data)

    # Ensure numeric columns are of correct type
    for df in [income_df, expenses_df]:
        for col in ['Actual Amount']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    total_income = income_df['Actual Amount'].sum()
    total_expenses = expenses_df['Actual Amount'].sum()
    net_income = total_income - total_expenses

    # Calculate savings rate
    savings_rate = (net_income / total_income) * 100 if total_income != 0 else 0
    # Calculate expense ratio
    expense_ratio = (total_expenses / total_income) * 100 if total_income != 0 else 0

    metrics = [
        html.P(f"Total Income: ${total_income:.2f}"),
        html.P(f"Total Expenses: ${total_expenses:.2f}"),
        html.P(f"Net Income: ${net_income:.2f}"),
        html.P(f"Savings Rate: {savings_rate:.2f}%"),
        html.P(f"Expense Ratio: {expense_ratio:.2f}%")
    ]

    return metrics
