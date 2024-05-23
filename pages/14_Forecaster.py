import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler


# Function to load data
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

# Function to add data features
def abDataFeatures(Data_002_FutureData):
    df = Data_002_FutureData.copy()
    df.reset_index(inplace=True)
    df['AUP'] = np.where(df['Quantity'].astype(float) != 0, 
                        df['Sell Out Revenue'].astype(float) / df['Quantity'].astype(float), 
                        0)
    df['Fin Month'] = pd.to_datetime(df['Fin Month'], format='%Y-%b')
    
    def ClassisificationFeatures(df):
        scaler = MinMaxScaler()
        df['NormalizedPrice'] = scaler.fit_transform(df[['AUP']])
        
        def categorize_forecast_price(row):
            if row['GrowthRate'] > 20:
                growth_category = 'High Demand'
            elif 10 <= row['GrowthRate'] <= 20:
                growth_category = 'Moderate Demand'
            elif 0 < row['GrowthRate'] < 10:
                growth_category = 'Low Demand'
            elif row['GrowthRate'] < 0:
                growth_category = 'Declining'
            else:
                growth_category = 'New Opportunities'
            
            if row['NormalizedPrice'] > 0.75:
                price_category = 'Premium'
            elif row['NormalizedPrice'] > 0.5:
                price_category = 'Above Average'
            elif row['NormalizedPrice'] > 0.25:
                price_category = 'Below Average'
            else:
                price_category = 'Budget'
            
            return f'{growth_category}, {price_category}'
        
        def categorize_by_normalized_price(row, percentiles):
            price = row['NormalizedPrice']
            if price <= percentiles['5th']:
                return 'Very Low'
            elif price <= percentiles['35th']:
                return 'Low'
            elif price <= percentiles['50th']:
                return 'Below Average'
            elif price <= percentiles['65th']:
                return 'Above Average'
            elif price <= percentiles['95th']:
                return 'High'
            else:
                return 'Very High'
        
        percentiles = {
            '5th': df['NormalizedPrice'].quantile(0.05),
            '35th': df['NormalizedPrice'].quantile(0.35),
            '50th': df['NormalizedPrice'].quantile(0.5),
            '65th': df['NormalizedPrice'].quantile(0.65),
            '95th': df['NormalizedPrice'].quantile(0.95)
        }
        
        df['PriceLevel'] = df.apply(categorize_by_normalized_price, axis=1, percentiles=percentiles)
        df['Fin Month'] = pd.to_datetime(df['Fin Month'])
        df.sort_values(by=['Key', 'Fin Month'], inplace=True)
        df['GrowthRate'] = df.groupby('Key')['Sell Out Revenue'].pct_change() * 100
        
        latest_month = df['Fin Month'].max()
        one_year_ago = latest_month - pd.DateOffset(months=12)
        df_last_12_months = df[df['Fin Month'] > one_year_ago]
        
        average_growth_last_12_months = df_last_12_months.groupby('Key')['GrowthRate'].mean().reset_index()
        average_growth_last_12_months.rename(columns={'GrowthRate': 'AvgGrowthRate'}, inplace=True)
        
        def categorize_growth(row, percentiles):
            growth = row['AvgGrowthRate']
            if growth <= percentiles['5th']:
                return 'Significantly Declining'
            elif growth <= percentiles['35th']:
                return 'Declining'
            elif growth <= percentiles['50th']:
                return 'Stable'
            elif growth <= percentiles['65th']:
                return 'Growing'
            elif growth <= percentiles['95th']:
                return 'Strong Growth'
            else:
                return 'Rapid Growth'
        
        percentiles = {
            '5th': average_growth_last_12_months['AvgGrowthRate'].quantile(0.05),
            '35th': average_growth_last_12_months['AvgGrowthRate'].quantile(0.35),
            '50th': average_growth_last_12_months['AvgGrowthRate'].quantile(0.5),
            '65th': average_growth_last_12_months['AvgGrowthRate'].quantile(0.65),
            '95th': average_growth_last_12_months['AvgGrowthRate'].quantile(0.95)
        }
        
        average_growth_last_12_months['GrowthCategory'] = average_growth_last_12_months.apply(categorize_growth, axis=1, percentiles=percentiles)
        df = pd.merge(df, average_growth_last_12_months[['Key', 'GrowthCategory']], on='Key', how='left')
        return df

    df = ClassisificationFeatures(df)
    df['Revenue_lag1'] = df.groupby(['Key','Fin Month'])['Sell Out Revenue'].shift(1)
    df.sort_values(by=['Key','Fin Month'], inplace=True)
    df['last_month_sales'] = df.groupby('Key')['Sell Out Revenue'].shift(1)
    df['sales_last_year'] = df.groupby('Key')['Sell Out Revenue'].shift(12)
    
    def calculate_cagr(ending_value, beginning_value, periods):
        if beginning_value <= 0 or ending_value < 0 or periods <= 0:
            return None
        else:
            return (ending_value/beginning_value)**(1/periods) - 1
    
    n = 2
    df['beginning_value'] = df.groupby('Key')['Sell Out Revenue'].transform(lambda x: x.shift(n*12))
    df['ending_value'] = df['Sell Out Revenue']
    df['CAGR'] = df.apply(lambda row: calculate_cagr(row['ending_value'], row['beginning_value'], n), axis=1)
    df.fillna(0, inplace=True)
    df.set_index(['Key','Fin Month'], inplace=True)
    columns_to_drop = ['index', 'level_0','Kilograms','Sell Out Revenue','NormalizedPrice']
    df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], axis=1)
    featureData = df
    featureData.sort_values(by=['Key','Fin Month'], inplace=True , ascending=False)   
    return featureData

# Start the Streamlit app
st.title('Data Analysis and Feature Enhancement Dashboard')

# Create a tabbed layout
tab1, tab2, tab3, tab4 = st.tabs(["Introduction", "Upload Data", "Data Features", "Dashboard"])

# Tab 1: Introduction
with tab1:
    st.header("Welcome to Our Machine Learning Services")
    st.markdown("""
        We provide a wide range of machine learning services to help businesses unlock the potential of their data.
        Our services include:
        - **Time Series Forecasting**: Predict future sales, inventory levels, and demand.
        - **Classification**: Categorize products, customers, and transactions to gain insights and drive decisions.
        - **Regression**: Predict continuous variables such as sales revenue and profit margins.
        - **Clustering**: Segment customers, products, or regions based on similarities.
        - **Anomaly Detection**: Identify unusual patterns and outliers in your data.
        - **Recommendation Systems**: Recommend products to customers based on their purchase history and preferences.
        - **Market Basket Analysis**: Discover frequently bought together items to inform cross-selling strategies.
        - **Reinforcement Learning**: Optimize decision-making over time for inventory management, dynamic pricing, and more.
        
        Explore the tabs to upload your data, process it, and visualize insights through our interactive dashboard.
    """)

# Tab 2: Data Upload
with tab2:
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        st.session_state['data'] = data
        st.write("Data uploaded successfully!")
        st.dataframe(data.head())

# Tab 3: Data Features
with tab3:
    if 'data' in st.session_state:
        st.write("Processing data to add features...")
        processed_data = abDataFeatures(st.session_state['data'])
        st.session_state['processed_data'] = processed_data
        st.write("Features added successfully!")
        st.dataframe(processed_data.head())
    else:
        st.error("Please upload data in the 'Upload Data' tab first.")

# Tab 4: Dashboard
with tab4:
    if 'processed_data' in st.session_state:
        st.header("Dashboard")
        processed_data = st.session_state['processed_data']
        
        # Visualization 1: Growth Category Distribution
        growth_category_dist = processed_data['GrowthCategory'].value_counts().reset_index()
        growth_category_dist.columns = ['GrowthCategory', 'Count']
        fig1 = px.bar(growth_category_dist, x='GrowthCategory', y='Count', title='Growth Category Distribution')
        st.plotly_chart(fig1)

        # Visualization 2: Price Level Distribution
        price_level_dist = processed_data['PriceLevel'].value_counts().reset_index()
        price_level_dist.columns = ['PriceLevel', 'Count']
        fig2 = px.bar(price_level_dist, x='PriceLevel', y='Count', title='Price Level Distribution')
        st.plotly_chart(fig2)
        
        # Visualization 3: Average Unit Price over Time
        avg_unit_price_over_time = processed_data.groupby('Fin Month')['AUP'].mean().reset_index()
        fig3 = px.line(avg_unit_price_over_time, x='Fin Month', y='AUP', title='Average Unit Price over Time')
        st.plotly_chart(fig3)
        
        # Visualization 4: Growth Rate Over Time
        growth_rate_over_time = processed_data.groupby('Fin Month')['GrowthRate'].mean().reset_index()
        fig4 = px.line(growth_rate_over_time, x='Fin Month', y='GrowthRate', title='Average Growth Rate over Time')
        st.plotly_chart(fig4)
        
        # Visualization 5: CAGR Distribution
        cagr_dist = processed_data['CAGR'].value_counts().reset_index()
        cagr_dist.columns = ['CAGR', 'Count']
        fig5 = px.bar(cagr_dist, x='CAGR', y='Count', title='CAGR Distribution')
        st.plotly_chart(fig5)
        
    else:
        st.error("Please process data in the 'Data Features' tab first.")
