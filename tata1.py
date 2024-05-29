import yfinance as yf
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.figure_factory as ff
from IPython.display import HTML


# Load the combined stock data CSV file
combined_data = pd.read_csv('combined_stock_data.csv')

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
        ),
        html.Div(id='stats-window', style={'backgroundColor': '#FFFFFF', 'padding': '10px', 'margin-top': '20px'})
    ]),
    dcc.Graph(id='stock-chart', style={'width': '100%', 'height': '600px'}),
    html.Div(id='stats-output')  # Placeholder for stats output
])


# Define the callback to update the stock chart based on the selected ticker
@app.callback(
    Output('stock-chart', 'figure'),
    Output('stats-window', 'children'),
    Input('ticker-dropdown', 'value')
)
def update_stock_chart_and_stats(selected_ticker):
    # Filter the data for the selected ticker
    filtered_data = combined_data[combined_data['Ticker'] == selected_ticker]
    
    # Convert the 'Date' column to datetime if it's not already
    filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
    
    # Sort the data by date
    filtered_data.sort_values(by='Date', inplace=True)
    
    # Prepare data for the bar graph
    bar_graph_data = filtered_data[['Date', 'Close']]
    
    # Prepare data for the line graph (stock prices)
    line_graph_data = filtered_data[['Date', 'Close']].copy()
    
    # Create a bar graph
    bar_fig = go.Figure(data=[go.Bar(x=bar_graph_data['Date'], y=bar_graph_data['Close'])])
    
    # Create a line graph for stock prices
    line_fig = go.Figure(data=[go.Scatter(x=line_graph_data['Date'], y=line_graph_data['Close'], mode='lines')])
    
    # Combine both figures horizontally
    fig = go.Figure(data=[go.Bar(x=bar_graph_data['Date'], y=bar_graph_data['Close']), go.Scatter(x=line_graph_data['Date'], y=line_graph_data['Close'], mode='lines')], layout=go.Layout(barmode='stack'))
    
    # Calculate stats
    max_value = filtered_data['Close'].max()
    min_value = filtered_data['Close'].min()
    total_volume = filtered_data['Volume'].sum()
    
    # Display stats with improved spacing
    stats_html = f"""
    <div style='font-size: 16px; margin-bottom: 10px;'>Max Value:</div>
    <div style='font-weight: bold; font-size: 18px;'>{max_value}</div>
    <br>
    <div style='font-size: 16px; margin-bottom: 10px;'>Min Value:</div>
    <div style='font-weight: bold; font-size: 18px;'>{min_value}</div>
    <br>
    <div style='font-size: 16px; margin-bottom: 10px;'>Total Volume:</div>
    <div style='font-weight: bold; font-size: 18px;'>{total_volume}</div>
    """
    
    # Return the HTML content as a JSON object
    return {'html': stats_html}

# app.layout = html.Div(style={'backgroundColor': '#F5F5F5', 'color': 'black'}, children=[
#     # Other layout elements...
#     html.Script("""
#     document.addEventListener('plotly_afterinit', function(eventData){
#         var statsOutputDiv = document.getElementById('stats-output');
#         var statsHtml = eventData.data.stats_output.html;
#         statsOutputDiv.innerHTML = statsHtml;
#     });
#     """)
# ])


# Run the Dash app on a different port (e.g., 8051)
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)

