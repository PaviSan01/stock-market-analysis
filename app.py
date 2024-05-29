import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os

# Load the combined stock data CSV file
combined_data = pd.read_csv('combined_stock_data.csv')
# 
# Initialize the Dash app
app = dash.Dash(__name__, title="Stock Market Analysis")

# Create a dropdown menu for selecting the ticker
ticker_options = [{'label': ticker, 'value': ticker} for ticker in combined_data['Ticker'].unique()]

# Define the layout of the dashboard with a milder background color for the title and search bar
app.layout = html.Div(style={'backgroundColor': '#F5F5F5', 'color': 'black'}, children=[
    html.H1("Stock Market Analysis", style={'textAlign': 'center'}),
    html.Div(style={'backgroundColor': '#EFEFEF', 'padding': '10px', 'borderRadius': '10px'}, children=[
        dcc.Dropdown(
            id='ticker-dropdown',
            options=ticker_options,
            value=ticker_options[0]['value'],
            style={'width': '100%', 'height': '40px', 'fontSize': '18px', 'color': 'black', 'backgroundColor': '#EFEFEF'}
        )
    ]),
    dcc.Graph(id='stock-chart', style={'width': '100%', 'height': '600px'})
])

# Define the callback to update the stock chart based on the selected ticker
@app.callback(
    Output('stock-chart', 'figure'),
    Input('ticker-dropdown', 'value')
)
def update_stock_chart(selected_ticker):
    filtered_data = combined_data[combined_data['Ticker'] == selected_ticker]
    fig = px.line(filtered_data, x='Date', y='Close', title=f'{selected_ticker} Stock Price')
    return fig

# Run the Dash app on a different port (e.g., 8051)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))


