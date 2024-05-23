import streamlit as st
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Demand Forecasting", page_icon="📊")

# Title of the page
st.title("Demand Forecasting")

# Upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Convert 'ProductID' to string
    df['ProductID'] = df['ProductID'].astype(str)

    # Function for demand forecasting using Holt-Winters Exponential Smoothing
    def forecast_demand(data, product_name, prediction_periods=12):
        product_data = data[data['ProductName'] == product_name][['Date', 'Sales']].set_index('Date')
        model = ExponentialSmoothing(product_data, trend='add', seasonal_periods=12)

        model_fit = model.fit()
        forecast = model_fit.forecast(prediction_periods)
        # Convert the index to dates
        forecast.index = pd.date_range(start=product_data.index[-1], periods=prediction_periods, freq='M').strftime('%Y-%m-%d')
        return forecast

    # Select product for demand forecasting
    product_name = st.selectbox("Select a Product Name for Demand Forecasting", df['ProductName'].unique())

    # Perform demand forecasting
    forecast_periods = st.slider("Select Number of Forecast Periods", min_value=1, max_value=24, value=12)
    forecast = forecast_demand(df, product_name, prediction_periods=forecast_periods)

    # Plot historical sales data and forecast
    product_data = df[df['ProductName'] == product_name].set_index('Date').iloc[-12:]
    plt.figure(figsize=(12, 6))
    plt.plot(product_data.index, product_data['Sales'], label='Actual Sales')
    plt.plot(forecast.index, forecast.values, label='Forecasted Sales', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.title(f'Sales Forecast for Product Name: {product_name}')
    plt.legend()
    st.pyplot(plt)

    # Display summary
    st.write("## Summary")
    st.write(f"Product Name: {product_name}")
    st.write(f"Number of Forecast Periods: {forecast_periods}")
    st.write("### Forecasted Demand:")
    st.write(forecast)
