import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.cluster import KMeans

# Set page configuration
st.set_page_config(page_title="Inventory Optimization2", page_icon="📈", layout="wide")

left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("fdLogo.png", width =200)

# Hide the Streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Sample data
data = {
    'ProductID': [101, 102, 103, 201, 202, 203],
    'ProductName': ['Brown Bread', 'White Bread', 'Unlisted Bread', 'Apple Juice', 'Pear Juice', 'Orange Juice'],
    'Category': ['Bread', 'Bread', 'Bread', 'Juice', 'Juice', 'Juice'],
    'StockLevel': [150, 200, 50, 60, 120, 80],
    'ReorderLevel': [50, 75, 30, 100, 60, 40],
    'LeadTimeDays': [10, 12, 15, 8, 10, 7],
    'UnitPrice': [5.99, 7.99, 9.99, 14.99, 19.99, 24.99]
}
sample_df = pd.DataFrame(data)

# Function for demand forecasting using Holt-Winters Exponential Smoothing
def forecast_demand(data, product_id, seasonal_periods=4, prediction_periods=4):
    product_data = data[data['ProductID'] == product_id]['StockLevel']
    model = ExponentialSmoothing(product_data, seasonal_periods=seasonal_periods, trend='add', seasonal='add')
    model_fit = model.fit()
    forecast = model_fit.forecast(prediction_periods)
    return forecast

# Function for ABC analysis
def abc_analysis(data):
    total_stock_value = data['StockLevel'] * data['UnitPrice']
    data['TotalStockValue'] = total_stock_value
    total_value = total_stock_value.sum()
    data['CumulativePercentage'] = total_stock_value.cumsum() / total_value
    data['Category'] = pd.cut(data['CumulativePercentage'], bins=[0, 0.7, 0.9, 1.0], labels=['A', 'B', 'C'])
    return data

# Function for K-means clustering
def kmeans_clustering(data, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters)
    data['Cluster'] = kmeans.fit_predict(data[['StockLevel']])
    return data

# Title of the page
st.title("Inventory Optimization")

# File upload section
st.header("Upload Your Inventory Data")
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Display file details
    st.write("## File Details")
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
    st.write(file_details)

    # Read the uploaded file
    if uploaded_file.type == "text/csv":
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    # Display a preview of the uploaded data
    st.write("## Data Preview")
    st.dataframe(df.head())

    # Perform initial data analysis
    st.write("## Data Analysis")
    st.write("### Basic Statistics")
    st.write(df.describe())

    # High-level KPIs
    st.write("## High-level KPIs")
    
    total_stock_value = (df['StockLevel'] * df['UnitPrice']).sum()
    total_products = df['ProductID'].nunique()
    avg_stock_level = df['StockLevel'].mean()
    total_reorder_level = df['ReorderLevel'].sum()
    avg_lead_time = df['LeadTimeDays'].mean()
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric(label="Total Stock Value", value=f"${total_stock_value:,.2f}")
    kpi2.metric(label="Total Products", value=total_products)
    kpi3.metric(label="Average Stock Level", value=f"{avg_stock_level:.2f}")

    kpi4, kpi5 = st.columns(2)
    kpi4.metric(label="Total Reorder Level", value=total_reorder_level)
    kpi5.metric(label="Average Lead Time (days)", value=f"{avg_lead_time:.2f}")

    # Analysis
    st.write("## Inventory Analysis")

    # Products below reorder level
    st.write("### Products Below Reorder Level")
    below_reorder = df[df['StockLevel'] < df['ReorderLevel']]
    st.dataframe(below_reorder)

    # Plotting stock levels
    st.write("### Stock Level Distribution")
    fig = px.histogram(df, x='StockLevel', nbins=20, title='Stock Level Distribution')
    st.plotly_chart(fig)

    # Identifying slow-moving products (low stock levels)
    st.write("### Slow-Moving Products")
    slow_moving = df[df['StockLevel'] < avg_stock_level]
    st.dataframe(slow_moving)

    # Identifying fast-moving products (high stock levels)
    st.write("### Fast-Moving Products")
    fast_moving = df[df['StockLevel'] >= avg_stock_level]
    st.dataframe(fast_moving)

    # Summary by category
    st.write("### Summary by Category")
    if 'Category' in df.columns:
        category_summary = df.groupby('Category').agg({
            'StockLevel': ['sum', 'mean'],
            'UnitPrice': 'mean',
            'ReorderLevel': 'sum',
            'LeadTimeDays': 'mean'
        }).reset_index()
        category_summary.columns = ['Category', 'Total Stock Level', 'Average Stock Level', 'Average Unit Price', 'Total Reorder Level', 'Average Lead Time (days)']
        st.dataframe(category_summary)
    else:
        st.write("Category column not found in the dataset.")

    # Demand Forecasting
    
    st.write("## Demand  Forecasting File Details")
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
    st.write(file_details)

    # Read the uploaded file
    if uploaded_file.type == "text/csv":
        dfDemandForecasting = pd.read_csv(uploaded_file)
    else:
        dfDemandForecasting = pd.read_excel(uploaded_file)
    
    st.write("## Demand Forecasting")
    product_id = st.selectbox("Select a Product ID for Demand Forecasting", dfDemandForecasting['ProductID'].unique())
    forecast_periods = st.slider("Select Number of Forecast Periods", min_value=1, max_value=12, value=4)
    forecast = forecast_demand(dfDemandForecasting, product_id, prediction_periods=forecast_periods)
    st.write(f"Forecasted Demand for ProductID {product_id}: {forecast}")


    # st.write("## Demand  Forecasting File Details")
    # file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
    # st.write(file_details)

    # # Read the uploaded file
    # if uploaded_file.type == "text/csv":
    #     dfDemandForecasting = pd.read_csv(uploaded_file)
    # else:
    #     dfDemandForecasting = pd.read_excel(uploaded_file)
    
    # st.write("## Demand Forecasting")
    # product_id = st.selectbox("Select a Product ID for Demand Forecasting", dfDemandForecasting['ProductID'].unique())
    # forecast_periods = st.slider("Select Number of Forecast Periods", min_value=1, max_value=12, value=4)
    # forecast = forecast_demand(dfDemandForecasting, product_id, prediction_periods=forecast_periods)
    # st.write(f"Forecasted Demand for ProductID {product_id}: {forecast}")
    # # ABC Analysis
    # st.write("## ABC Analysis")
    # abc_df = abc_analysis(df)
    # st.write(abc_df)

    # # K-means Clustering
    # st.write('## K-means Clustering')
    # n_clusters = st.slider("Select Number of Clusters for K-means Clustering", min_value=2, max_value=5, value=3)
    # kmeans_df = kmeans_clustering(df, n_clusters=n_clusters)
    # st.write(kmeans_df)

else:
    # Display sample data and analysis
    st.write("## Sample Data and Analysis")
    st.write("### Sample Data")
    st.dataframe(sample_df)

    # Demand Forecasting for sample data
    st.write("### Demand Forecasting for Sample Data")
    sample_product_id = st.selectbox("Select a Product ID for Demand Forecasting (Sample Data)", sample_df['ProductID'].unique())
    sample_forecast_periods = st.slider("Select Number of Forecast Periods (Sample Data)", min_value=1, max_value=12, value=4)
    sample_forecast = forecast_demand(sample_df, sample_product_id, prediction_periods=sample_forecast_periods)
    st.write(f"Forecasted Demand for ProductID {sample_product_id}: {sample_forecast}")

    # ABC Analysis for sample data
    st.write("### ABC Analysis for Sample Data")
    sample_abc_df = abc_analysis(sample_df)
    st.write(sample_abc_df)

    # K-means Clustering for sample data
    st.write("### K-means Clustering for Sample Data")
    sample_n_clusters = st.slider("Select Number of Clusters for K-means Clustering (Sample Data)", min_value=2, max_value=5, value=3)
    sample_kmeans_df = kmeans_clustering(sample_df, n_clusters=sample_n_clusters)
    st.write(sample_kmeans_df)

