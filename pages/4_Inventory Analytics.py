import streamlit as st
import pandas as pd
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.cluster import KMeans
import streamlit_shadcn_ui as ui
from st_aggrid import AgGrid, GridOptionsBuilder

# Set page configuration
st.set_page_config(page_title="Inventory Analytics", page_icon="📈", layout="wide")

st.image("fdLogo.png")

tab1, tab2, tab3, tab4 = st.tabs(["Main", "Analytics", "Alerts", "Recommendations"])

# Hide the Streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


with tab1:  
    st.write("MAin Page")

with tab2:
    # Title of the page
    st.title("Inventory Analytics")
    
    
    if 'inventory_data' in st.session_state.uploaded_files:
        df = st.session_state.uploaded_files['inventory_data']
     
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
        gb.configure_side_bar()  # Add a sidebar
        gb.configure_default_column(editable=True, groupable=True)
        
        df['TotalRevenue'] = df['StockLevel'] * df['UnitPrice'] 
        df['AvgRevenuePerCategory'] = df.groupby('Category')['TotalRevenue'].transform('mean')
        # Calculate measures
        total_revenue = df["StockLevel"] * df["UnitPrice"]
        average_revenue_per_product = total_revenue.mean()
        total_stock_level = df["StockLevel"].sum()
        total_reorder_level = df["ReorderLevel"].sum()
        average_lead_time_days = df["LeadTimeDays"].mean()
        average_unit_price = df["UnitPrice"].mean()
        # Calculate measures
        total_revenue = df['StockLevel'] * df['UnitPrice']
        total_stock_value = df['StockLevel'] * df['UnitPrice']
        average_lead_time = df['LeadTimeDays'].mean()
        reorder_ratio = df['ReorderLevel'].sum() / df['StockLevel'].sum()
        average_price = df['UnitPrice'].mean()
        total_products = len(df)
        max_revenue_product = df.loc[df['TotalRevenue'].idxmax()]
        max_AvgRrevenue_productrevenue_product = df.loc[df['AvgRevenuePerCategory'].idxmax()]    
        # Populate Metric Cards
        metrics = [
            ("Total Revenue", f"ZAR {total_revenue.sum():,.2f}", 
                 f"The product with the highest revenue is '{max_revenue_product['ProductName']}' with a total revenue of ZAR {max_revenue_product['TotalRevenue']:.2f}"),
            ("Average Revenue per Product", f"ZAR {average_revenue_per_product:.2f}", 
                 f"The category with the highest Avgerage  revenue is '{max_AvgRrevenue_productrevenue_product['Category']}' with an average revenue of ZAR {max_AvgRrevenue_productrevenue_product['TotalRevenue']:.2f}"),
            ("Total Stock Level", f"{total_stock_level}", ""),
            ("Total Reorder Level", f"{total_reorder_level}", ""),
            ("Reorder Ratio", f"{reorder_ratio.mean():.2%}", ""),
            ("Average Lead Time Days", f"{average_lead_time_days:.2f}", ""),
            ("Average Unit Price", f"ZAR {average_unit_price:.2f}", "")
        ]
        
        cols = st.columns(3)
        for i, (title, content, description) in enumerate(metrics):
            with cols[i % 3]:
                ui.metric_card(title=title, content=content, description=description, key=f"card{i+1}")
                # Display a preview of the uploaded data
        
        st.write("## Data Preview")
        st.dataframe(df)
        
        grid_options = gb.build()
        AgGrid(df, gridOptions=grid_options)
        
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
                'LeadTimeDays': 'mean',
                'TotalRevenue':'sum'
            }).reset_index()
            category_summary.columns = ['Category', 'Total Stock Level', 'Average Stock Level', 'Average Unit Price', 'Total Reorder Level', 'Average Lead Time (days)','Total Revenue']
            st.dataframe(category_summary)
        else:
            st.write("Category column not found in the dataset.")
    
    
        def kpi_with_color(value, threshold):
            if value >= threshold:
                color = "green"
            else:
                color = "red"
            return f'<span style="color:{color};font-size:100px">{value}</span>'
        
        # Example usage
        threshold = 50
        current_value = 60
        st.write(f"Current Value: {kpi_with_color(current_value, threshold)}", unsafe_allow_html=True)
    else:
        st.write("Please upload a file to begin the inventory optimization process.")
