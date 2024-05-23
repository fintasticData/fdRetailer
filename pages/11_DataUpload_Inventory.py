import streamlit as st
import pandas as pd
import plotly.express as px

# Ensure the page configuration is appropriate for this section
st.set_page_config(page_title="Inventory Analysis", page_icon="📈", layout="wide")

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image("fdLogo.png", width=200)

# Hide the Streamlit header and footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Title of the page
st.title("Inventory Optimization Analysis")

# Check if the inventory data is uploaded
if 'inventory_data' in st.session_state.uploaded_files:
    df = st.session_state.uploaded_files['inventory_data']

    # Create columns for layout
    col1, col2, col3 = st.columns([2, 3, 2])

    with col1:
        # Required fields for your template
        required_fields = ['ProductID', 'StockLevel', 'UnitPrice', 'ReorderLevel', 'LeadTimeDays']

        # Create a dictionary to store the mappings
        field_mappings = {}

        st.write("## Map Your Data Fields to Our Template")

        # Create select boxes for each required field
        for field in required_fields:
            field_mappings[field] = st.selectbox(f"Select the column for {field}", options=df.columns.tolist())

    with col2:
        st.write("### Data Before Mapping")
        st.dataframe(df.head())

        # Apply the field mappings
        mapped_df = df.rename(columns=field_mappings)

        st.write("### Data After Mapping")
        st.dataframe(mapped_df.head())

        # Store the mapped data in session state
        st.session_state['mapped_inventory_data'] = mapped_df

    # High-level KPIs and further analysis can follow
    st.write("## Data Analysis")
    st.write("### Basic Statistics")
    st.write(mapped_df.describe())

    # High-level KPIs
    st.write("## High-level KPIs")

    total_stock_value = (mapped_df['StockLevel'] * mapped_df['UnitPrice']).sum()
    total_products = mapped_df['ProductID'].nunique()
    avg_stock_level = mapped_df['StockLevel'].mean()
    total_reorder_level = mapped_df['ReorderLevel'].sum()
    avg_lead_time = mapped_df['LeadTimeDays'].mean()

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
    below_reorder = mapped_df[mapped_df['StockLevel'] < mapped_df['ReorderLevel']]
    st.dataframe(below_reorder)

    # Plotting stock levels
    st.write("### Stock Level Distribution")
    fig = px.histogram(mapped_df, x='StockLevel', nbins=20, title='Stock Level Distribution')
    st.plotly_chart(fig)

    # Identifying slow-moving products (low stock levels)
    st.write("### Slow-Moving Products")
    slow_moving = mapped_df[mapped_df['StockLevel'] < avg_stock_level]
    st.dataframe(slow_moving)

    # Identifying fast-moving products (high stock levels)
    st.write("### Fast-Moving Products")
    fast_moving = mapped_df[mapped_df['StockLevel'] >= avg_stock_level]
    st.dataframe(fast_moving)

    # Summary by category
    st.write("### Summary by Category")
    if 'Category' in mapped_df.columns:
        category_summary = mapped_df.groupby('Category').agg({
            'StockLevel': ['sum', 'mean'],
            'UnitPrice': 'mean',
            'ReorderLevel': 'sum',
            'LeadTimeDays': 'mean'
        }).reset_index()
        category_summary.columns = ['Category', 'Total Stock Level', 'Average Stock Level', 'Average Unit Price', 'Total Reorder Level', 'Average Lead Time (days)']
        st.dataframe(category_summary)
    else:
        st.write("Category column not found in the dataset.")
else:
    st.write("Please upload the inventory data on the Data Upload page to begin the analysis.")
