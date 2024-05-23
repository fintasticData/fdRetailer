# -*- coding: utf-8 -*-
"""
Created on Tue May 21 18:44:29 2024

@author: dell
"""


import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from st_aggrid import AgGrid, GridOptionsBuilder

# Set page configuration
st.set_page_config(page_title="FMCG Sales Dashboard", page_icon="📊", layout="wide")

# Display logo
st.image("fdLogo.png")

# Hide the Streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


data = st.session_state.uploaded_files['marketing_data']

# Title of the page
st.title("FMCG Sales Dashboard")

# Display links and info
st.write("### Dataset")
st.write(data.head())

# Column selection
st.write("### Columns")
date_col = st.selectbox("Select Date Column", data.columns)
target_col = st.selectbox("Select Target Column", data.columns)

# Combine Product, Customer, and Territory for selection
st.write("### Filtering")

combined_options = (data['Product'] + ' | ' + data['Customer'] + ' | ' + data['Territory']).unique()
selected_combined = st.selectbox("Select Product | Customer | Territory", ['All'] + list(combined_options))

# Filter data based on the combined selection
if selected_combined != 'All':
    selected_product, selected_customer, selected_territory = selected_combined.split(' | ')
    filtered_data = data[(data['Product'] == selected_product) & 
                         (data['Customer'] == selected_customer) & 
                         (data['Territory'] == selected_territory)]
else:
    filtered_data = data

# Brand filter
unique_brands = data['Brand'].unique()
selected_brand = st.selectbox("Select Brand", ['All'] + list(unique_brands))

if selected_brand != 'All':
    filtered_data = filtered_data[filtered_data['Brand'] == selected_brand]

# Resampling
st.write("### Resampling")
resample_option = st.selectbox("Resample Data", ["None", "Monthly", "Quarterly", "Yearly"])
if resample_option != "None":
    filtered_data[date_col] = pd.to_datetime(filtered_data[date_col])
    if resample_option == "Monthly":
        filtered_data = filtered_data.resample('M', on=date_col).sum().reset_index()
    elif resample_option == "Quarterly":
        filtered_data = filtered_data.resample('Q', on=date_col).sum().reset_index()
    elif resample_option == "Yearly":
        filtered_data = filtered_data.resample('Y', on=date_col).sum().reset_index()

# Display the filtered data
st.write("## Filtered Data")
st.write(filtered_data)

# Initialize AgGrid
gb = GridOptionsBuilder.from_dataframe(filtered_data)
gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
gb.configure_side_bar()  # Add a sidebar
gb.configure_default_column(editable=True, groupable=True)
grid_options = gb.build()
AgGrid(filtered_data, gridOptions=grid_options)

# Metrics Calculation
filtered_data['TotalRevenue'] = filtered_data['SalesVolume'] * filtered_data['UnitPrice']
total_revenue = filtered_data['TotalRevenue'].sum()
average_revenue_per_product = filtered_data['TotalRevenue'].mean()
total_sales_volume = filtered_data['SalesVolume'].sum()
average_unit_price = filtered_data['UnitPrice'].mean()

# High-level KPIs
st.write("## High-level KPIs")
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(label="Total Revenue", value=f"${total_revenue:,.2f}")
kpi2.metric(label="Average Revenue per Product", value=f"${average_revenue_per_product:,.2f}")
kpi3.metric(label="Total Sales Volume", value=f"{total_sales_volume:,}")

# Products below reorder level
st.write("### Products Below Reorder Level")
below_reorder = filtered_data[filtered_data['SalesVolume'] < filtered_data['ReorderLevel']]
st.dataframe(below_reorder)

# Plotting sales distribution
st.write("### Sales Volume Distribution")
fig = px.histogram(filtered_data, x='SalesVolume', nbins=20, title='Sales Volume Distribution')
st.plotly_chart(fig)

# Identifying slow-moving products (low sales volume)
st.write("### Slow-Moving Products")
slow_moving = filtered_data[filtered_data['SalesVolume'] < filtered_data['SalesVolume'].mean()]
st.dataframe(slow_moving)

# Identifying fast-moving products (high sales volume)
st.write("### Fast-Moving Products")
fast_moving = filtered_data[filtered_data['SalesVolume'] >= filtered_data['SalesVolume'].mean()]
st.dataframe(fast_moving)

# Summary by category
st.write("### Summary by Category")
if 'Category' in filtered_data.columns:
    category_summary = filtered_data.groupby('Category').agg({
        'SalesVolume': ['sum', 'mean'],
        'UnitPrice': 'mean',
        'TotalRevenue': 'sum'
    }).reset_index()
    category_summary.columns = ['Category', 'Total Sales Volume', 'Average Sales Volume', 'Average Unit Price', 'Total Revenue']
    st.dataframe(category_summary)
else:
    st.write("Category column not found in the dataset.")

# Future sales forecast
st.write("## Future Sales Forecast")

# Select the time series parameters
forecast_periods = st.number_input("Enter the number of periods for forecasting:", min_value=1, max_value=24, value=12)

# Prepare the data for forecasting
if date_col and target_col:
    filtered_data[date_col] = pd.to_datetime(filtered_data[date_col])
    ts_data = filtered_data.set_index(date_col)[target_col].asfreq('M')
    
    # Apply Holt-Winters Exponential Smoothing
    model = ExponentialSmoothing(ts_data, seasonal='add', seasonal_periods=12)
    model_fit = model.fit()
    forecast = model_fit.forecast(forecast_periods)
    
    # Plot the forecast
    fig = px.line(x=forecast.index, y=forecast.values, labels={'x': 'Date', 'y': 'Sales'}, title='Sales Forecast')
    st.plotly_chart(fig)
else:
    st.write("Please select valid Date and Target columns for forecasting.")

# Save experiment button
def save_experiment(data, file_name="experiment_result.csv"):
    data.to_csv(file_name, index=False)
    st.success(f"Experiment saved to {file_name}")

if st.button("Save Experiment"):
    save_experiment(filtered_data)

