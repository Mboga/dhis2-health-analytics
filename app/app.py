# Import necessary libraries
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import sys # Keep sys if you want to print to stderr

# Initialize app outside the try block, so it's always defined
app = Dash(__name__)
server = app.server # Gunicorn needs this

df = pd.DataFrame() # Initialize an empty DataFrame
data_load_error = None

try:
    # --- 1. Load the data into Pandas ---
    df = pd.read_csv('dhis2_data.csv')
    print("Data loaded successfully! Head of DataFrame:")
    print(df.head(), file=sys.stderr) # Print to stderr for Gunicorn logs
    print("\nDataFrame Info:", file=sys.stderr)
    df.info(buf=sys.stderr) # Ensure info also goes to stderr

    # --- 2. Data Cleaning and Preparation ---
    df['reported_value'] = pd.to_numeric(df['reported_value'], errors='coerce')
    df.dropna(subset=['reported_value'], inplace=True)
    df['period_start_date'] = pd.to_datetime(df['period_start_date'])

    required_cols = ['organisation_unit_name', 'data_element_name', 'period_iso', 'reported_value']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing one or more required columns for visualization: {required_cols}")

    target_data_element = 'Measles doses given'
    df_filtered = df[df['data_element_name'] == target_data_element].copy()

    if df_filtered.empty:
        print(f"Warning: No data found for '{target_data_element}'. Please check the data element name in your CSV.", file=sys.stderr)
        if not df['data_element_name'].empty:
            target_data_element = df['data_element_name'].iloc[0]
            df_filtered = df[df['data_element_name'] == target_data_element].copy()
            print(f"Using '{target_data_element}' for visualization instead.", file=sys.stderr)
        else:
            print("No data elements found in the CSV. Cannot create a plot.", file=sys.stderr)
            # If no data elements at all, set an error
            data_load_error = "No data elements found in the CSV. Cannot create a plot."

except FileNotFoundError:
    data_load_error = "Error: 'dhis2_data.csv' not found. Please make sure the data file is present."
    print(data_load_error, file=sys.stderr)
except Exception as e:
    data_load_error = f"An unexpected error occurred during data processing: {e}"
    print(data_load_error, file=sys.stderr)


# --- Define Layout based on data loading success/failure ---
if data_load_error:
    app.layout = html.Div([
        html.H1("Application Error"),
        html.P(data_load_error),
        html.P("Please check the server logs for more details.")
    ])
else:
    # Original successful layout
    app.layout = html.Div([
        html.H1("DHIS2 Sierra Leone Health Data Analysis"),

        html.Div([
            html.Label("Select Data Element:"),
            dcc.Dropdown(
                id='data-element-dropdown',
                options=[{'label': i, 'value': i} for i in df['data_element_name'].unique()],
                value=target_data_element, # Set a default value
                clearable=False
            ),
        ]),
        html.Div([
            html.Label("Select Period (Year-Month):"),
            dcc.Dropdown(
                id='period-dropdown',
                options=[], # Options will be set by callback
                value=None, # Initial value will be set by callback
                clearable=False
            ),
        ]),

        dcc.Graph(id='bar-chart')
    ])

    # Only define callbacks if data loaded successfully
    @app.callback(
        Output('period-dropdown', 'options'),
        Output('period-dropdown', 'value'),
        Input('data-element-dropdown', 'value')
    )
    def set_period_options(selected_data_element):
        if selected_data_element:
            periods = df[df['data_element_name'] == selected_data_element]['period_iso'].unique()
            periods.sort()
            options = [{'label': p, 'value': p} for p in periods]
            default_value = periods[0] if periods.size > 0 else None
            return options, default_value
        return [], None

    @app.callback(
        Output('bar-chart', 'figure'),
        Input('data-element-dropdown', 'value'),
        Input('period-dropdown', 'value')
    )
    def update_graph(selected_data_element, selected_period_iso):
        if not selected_data_element or not selected_period_iso:
            return {}

        filtered_df = df[
            (df['data_element_name'] == selected_data_element) &
            (df['period_iso'] == selected_period_iso)
        ].copy()

        aggregated_df = filtered_df.groupby('organisation_unit_name')['reported_value'].sum().reset_index()

        fig = px.bar(
            aggregated_df,
            x='organisation_unit_name',
            y='reported_value',
            title=f'{selected_data_element} by Organization Unit ({selected_period_iso})',
            labels={
                'organisation_unit_name': 'Organization Unit',
                'reported_value': 'Reported Value'
            }
        )
        fig.update_layout(xaxis_tickangle=-45)
        return fig

# Gunicorn will import this module and find `app.server` directly.
# The `server` variable is already defined globally.