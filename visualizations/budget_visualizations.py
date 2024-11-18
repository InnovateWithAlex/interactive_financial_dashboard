# visualizations/budget_visualizations.py

import plotly.graph_objects as go

def create_budget_vs_actual_chart(merged_data):
    """
    Create a bar chart comparing budgeted amounts to actual spending per category.
    """
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=merged_data['Category'],
        y=merged_data['Budgeted Amount'],
        name='Budgeted Amount'
    ))
    fig.add_trace(go.Bar(
        x=merged_data['Category'],
        y=merged_data['Actual Amount'],
        name='Actual Amount'
    ))
    fig.update_layout(
        title='Budget vs. Actual Spending',
        xaxis_title='Category',
        yaxis_title='Amount',
        barmode='group',
        template='plotly_dark'
    )
    return fig
