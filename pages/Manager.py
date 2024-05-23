import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(page_title="Manager", page_icon="📈", layout="wide")
st.image("fdLogo.png")
st.title("MD Dashboard")
st.write("Welcome to the Managing Director's Dashboard. Here you can view key performance indicators and metrics that provide a comprehensive overview of the business performance.")

# Sample data
np.random.seed(42)
dates = pd.date_range(start='2021-01-01', periods=100)
sales_data = pd.DataFrame({
    'Date': dates,
    'Sales': np.random.poisson(300, 100),
    'Inventory': np.random.poisson(200, 100)
})

# Functions to calculate KPIs
def calculate_kpis(sales_multiplier, inventory_multiplier):
    total_sales = sales_data['Sales'].sum() * sales_multiplier
    total_inventory = sales_data['Inventory'].sum() * inventory_multiplier
    return total_sales, total_inventory

# Functions to create charts
def create_sales_chart(sales_multiplier):
    adjusted_sales = sales_data['Sales'] * sales_multiplier
    chart_data = sales_data.copy()
    chart_data['Adjusted Sales'] = adjusted_sales
    sales_chart = alt.Chart(chart_data).mark_line().encode(
        x='Date',
        y='Adjusted Sales'
    ).properties(
        title='Adjusted Sales Over Time',
        width=600,
        height=400
    )
    return sales_chart

def create_inventory_chart(inventory_multiplier):
    adjusted_inventory = sales_data['Inventory'] * inventory_multiplier
    chart_data = sales_data.copy()
    chart_data['Adjusted Inventory'] = adjusted_inventory
    inventory_chart = alt.Chart(chart_data).mark_line().encode(
        x='Date',
        y='Adjusted Inventory'
    ).properties(
        title='Adjusted Inventory Over Time',
        width=600,
        height=400
    )
    return inventory_chart


tab1, tab2, tab3, tab4, tab5, tab6, tab7,tab8, tab9, tab10 = st.tabs(["Cover","KPI", "Competition", "Sales","Costs","OPEX","Profit","Assets","Owing","Position"])



with tab1:
  
    # Page Title
    st.title("One-Pager: Key Components of Retail Analytics")
    
    # Retail Forecasting
    st.header("Retail Forecasting")
    st.write("""
    Retail forecasting is the process of predicting future sales and inventory needs based on historical data, market trends, and consumer behavior. Accurate retail forecasting helps businesses optimize stock levels, manage supply chains, and improve customer satisfaction by ensuring product availability.
    """)
    st.subheader("Key Benefits:")
    st.write("""
    - Enhanced inventory management
    - Better demand planning
    - Reduced stockouts and overstock situations
    """)
    
    # Inventory Optimization
    st.header("Inventory Optimization")
    st.write("""
    Inventory optimization involves maintaining the right balance of stock to meet customer demand while minimizing costs. This process uses sophisticated algorithms and analytics to determine optimal inventory levels, reorder points, and safety stock.
    """)
    st.subheader("Key Benefits:")
    st.write("""
    - Lower carrying costs
    - Increased inventory turnover
    - Improved cash flow
    """)
    
    # Demand Forecasting
    st.header("Demand Forecasting")
    st.write("""
    Demand forecasting predicts future consumer demand using historical sales data, market trends, and economic indicators. This allows retailers to align their inventory, production, and distribution strategies with expected demand patterns.
    """)
    st.subheader("Key Benefits:")
    st.write("""
    - Improved supply chain efficiency
    - Enhanced production planning
    - Better customer service through availability of in-demand products
    """)
    
    # Sales Analysis
    st.header("Sales Analysis")
    st.write("""
    Sales analysis involves examining historical sales data to identify trends, patterns, and insights. This analysis helps retailers understand what drives sales, evaluate the effectiveness of promotions, and make data-driven decisions.
    """)
    st.subheader("Key Benefits:")
    st.write("""
    - Identification of sales trends and seasonality
    - Insight into product performance
    - Enhanced strategic planning and decision-making
    """)
    
    # Customer Segmentation
    st.header("Customer Segmentation")
    st.write("""
    Customer segmentation is the practice of dividing a customer base into distinct groups based on demographics, purchasing behavior, and other relevant criteria. This segmentation allows for targeted marketing and personalized customer experiences.
    """)
    st.subheader("Key Benefits:")
    st.write("""
    - Improved marketing effectiveness
    - Enhanced customer engagement
    - Increased customer loyalty and retention
    """)
    
    # Price Optimization
    st.header("Price Optimization")
    st.write("""
    Price optimization uses data analytics to determine the ideal pricing strategy for maximizing profits while maintaining competitiveness. This involves analyzing various factors such as market conditions, competitor pricing, and customer willingness to pay.
    """)
    st.subheader("Key Benefits:")
    st.write("""
    - Maximized revenue and profit margins
    - Competitive pricing strategies
    - Better alignment with market demand
    """)
    
    # Conclusion
    st.header("Conclusion")
    st.write("""
    Implementing these key components of retail analytics enables businesses to make informed decisions, optimize operations, and enhance customer satisfaction. By leveraging data-driven insights, retailers can stay ahead of market trends, efficiently manage resources, and drive sustainable growth.
    """)


with tab2:  
    # Sample data for KPIs and relevant indicators
    metrics = [
        ("Total Sales", "$1,500,000", "Total sales for the current month.", "▲ 5%", "Compared to last month", "green", "total_sales", "With a 5% increase in total sales compared to last month, consider analyzing sales trends to identify top-performing products or regions. Implement targeted marketing strategies using ML techniques like customer segmentation to drive further sales growth."),
        ("Beverage Category Sales", "$750,000", "Sales of beverages for the current month.", "▲ 3%", "Compared to last month", "orange", "beverage_sales", "The 3% increase in beverage sales indicates a positive trend. Use ML for demand forecasting to optimize inventory and ensure stock availability of popular beverages, maximizing sales potential."),
        ("Market Share", "25%", "Current market share in the FMCG beverage sector.", "▼ 1%", "Compared to last quarter", "red", "market_share", "The slight decrease in market share could be mitigated by analyzing competitors' strategies using ML-based competitive intelligence. Implement targeted campaigns or product enhancements to regain market share."),
        ("Profit Margin", "18%", "Profit margin for the current quarter.", "▲ 2%", "Compared to last quarter", "green", "profit_margin", "With an increase of 2% in profit margin, consider using ML for dynamic pricing strategies based on demand and competitor pricing, optimizing margins further."),
        ("Inventory Levels", "10,000 units", "Current inventory levels of top-selling products.", "▲ 500 units", "Compared to last month", "orange", "inventory_levels", "The increase of 500 units in inventory suggests efficient stock management. Utilize ML for predictive maintenance to ensure optimal inventory levels and minimize stockouts."),
        ("Customer Satisfaction", "4.5/5", "Average customer satisfaction score from recent surveys.", "▲ 0.2", "Compared to last month", "green", "customer_satisfaction", "With an average score of 4.5/5, maintain this high satisfaction level by using sentiment analysis through ML on customer feedback to identify areas for improvement."),
        ("Demand Forecast", "12,000 units", "Forecasted demand for the next month.", "▲ 10%", "Compared to last forecast", "green", "demand_forecast", "The 10% increase in demand forecast indicates growing market demand. Use ML techniques such as time series forecasting to improve accuracy and adjust inventory and production planning accordingly."),
        ("Total Expenses", "$500,000", "Total expenses for the current month.", "▲ 4%", "Compared to last month", "red", "total_expenses", "Despite a 4% increase in total expenses, ML can be used for cost optimization through predictive analytics, identifying areas where costs can be reduced without compromising quality."),
        ("Sales per Rep", "$50,000", "Average sales per sales representative.", "▲ 6%", "Compared to last month", "green", "sales_per_rep", "With a 6% increase in sales per representative, consider using ML for sales performance analysis to identify top-performing reps and share best practices across the team for further improvement."),
        ("Cost of Goods Sold (COGS)", "$400,000", "Total COGS for the current month.", "▲ 3%", "Compared to last month", "orange", "cogs", "The 3% increase in COGS warrants a closer look at production costs. Implement ML-driven process optimization to reduce production costs and improve margins."),
        ("Operating Income", "$300,000", "Operating income for the current month.", "▲ 2%", "Compared to last month", "green", "operating_income", "With a 2% increase in operating income, consider using ML for operational efficiency analysis, identifying areas where processes can be streamlined for further cost savings."),
        ("Return on Investment (ROI)", "15%", "ROI for the current month.", "▲ 1%", "Compared to last month", "green", "roi", "The 1% increase in ROI indicates positive returns. Use ML for marketing attribution to identify the most effective marketing channels and allocate resources accordingly for higher ROI.")
    ]
    
    # Light/Dark mode selection
    mode = st.toggle("Select Mode")
    
    # Set styles based on the selected mode
    if mode:
        text_color = "white"
        background_color = "#333"
        border_color = "silver"
    else:
        text_color = "black"
        background_color = "white"
        border_color = "black"
    
    
    
    # Create columns for metrics
    cols = st.columns(3)
    for i, (title, content, description, indicator, indicator_desc, color, page, summary) in enumerate(metrics):
        with cols[i % 3]:
            # Combining KPI and indicator within a single HTML element and adding a border
            st.markdown(f"""
            <div style='border: 5px solid {border_color}; padding: 20px; border-radius: 10px; margin-bottom: 10px; background-color: {background_color}; cursor: pointer;' onclick="window.location.href='?page={page}'">
                <div style='display: flex; align-items: left;padding: 10px;'>
                    <div style='flex-grow: 2; color: {text_color};'>
                        <p style='color: {color};margin: 0; font-size: 1.5em;'>{indicator}</p>
                        <p style='color: {text_color}; margin: 0;'>{indicator_desc}</p>
                        <br> </br>
                    </div>
                    <div style='flex-grow: 0; text-align: left;padding: 20px;'>
                        <h4 style='margin: 0;color: {text_color}'>{title}</h4>
                        <span style='color: {text_color}; font-size: 2.5em; font-weight: bold;'>{content}</span>
                        <p style='color: {text_color}; margin: 0;'>{description}</p>
                        <p style='color: {text_color}; margin: 0;'>{summary}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)


with tab3:  
    st.title('Allens Competitive Analysis Dashboard')
    
    # Step 1: Upload CSV file
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        # Step 2: Data Preprocessing
        df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
        df['PricePerLiter'] = pd.to_numeric(df['PricePerLiter'], errors='coerce')
        df.fillna(0, inplace=True)
        
        # Creating FinDate column
        df['FinDate'] = pd.to_datetime(df['Fin Month'] + ' ' + df['Fin Year'].astype(str))
        
        # Filter out negative Sell Out Revenue values
        df = df[df['Sell Out Revenue'] >= 0]
        
        # Step 3: Dashboard Elements
        st.subheader('Sales Performance Comparison')
        sales_performance = df.groupby(['Manufacturer', 'Brand'])['Sell Out Revenue'].sum().reset_index()
        st.dataframe(sales_performance)
        
        fig1 = px.bar(sales_performance, x='Brand', y='Sell Out Revenue', color='Manufacturer', barmode='group', title="Sales Performance Comparison")
        st.plotly_chart(fig1)
        
        st.subheader('Market Share Analysis')
        market_share = df.groupby(['Manufacturer'])['Sell Out Revenue'].sum().reset_index()
        market_share['Market Share'] = market_share['Sell Out Revenue'] / market_share['Sell Out Revenue'].sum() * 100
        st.dataframe(market_share)
        
        fig2 = px.pie(market_share, names='Manufacturer', values='Market Share', title='Market Share Analysis')
        st.plotly_chart(fig2)
        
        st.subheader('Customer Segmentation')
        customer_segmentation = df.groupby(['Customer'])['Sell Out Revenue'].sum().reset_index()
        st.dataframe(customer_segmentation)
        
        fig3 = px.bar(customer_segmentation, x='Customer', y='Sell Out Revenue', title='Customer Segmentation')
        st.plotly_chart(fig3)
        
        st.subheader('Location Analysis')
        location_analysis = df.groupby(['Territory'])['Sell Out Revenue'].sum().reset_index()
        st.dataframe(location_analysis)
        
        fig4 = px.choropleth(location_analysis, locations='Territory', locationmode='country names', color='Sell Out Revenue', title='Location Analysis')
        st.plotly_chart(fig4)
        
        st.subheader('Product Performance')
        product_performance = df.groupby(['Brand', 'Item'])['Sell Out Revenue'].sum().reset_index()
        st.dataframe(product_performance)
        
        fig5 = px.bar(product_performance, x='Item', y='Sell Out Revenue', color='Brand', title='Product Performance', barmode='group')
        st.plotly_chart(fig5)
        
        st.subheader('Clibos Price Analysis')
        price_analysis = df.groupby(['Brand', 'Item'])['UnitPrice'].mean().reset_index()
        st.dataframe(price_analysis)
        
        st.subheader('Trend Analysis')
        trend_analysis = df.groupby(['FinDate', 'Manufacturer'])['Sell Out Revenue'].sum().reset_index()
        trend_analysis = trend_analysis.sort_values('FinDate')
        fig6 = px.line(trend_analysis, x='FinDate', y='Sell Out Revenue', color='Manufacturer', title='Trend Analysis')
        st.plotly_chart(fig6)
        
        st.subheader('Price vs. Sales')
        fig7 = px.scatter(df, x='UnitPrice', y='Sell Out Revenue', color='Manufacturer', title='Price vs. Sales', size='Sell Out Revenue', hover_data=['Brand', 'Item'])
        st.plotly_chart(fig7)
        
        st.subheader('Recommendations')
        st.write("With these insights, you can adjust your strategies to stay competitive. Analyze the sales performance to identify top products, understand your market share, optimize inventory and pricing strategies, and monitor trends to anticipate changes in demand.")
    else:
        st.write("Please upload a CSV file to see the analysis.")
    
with tab4:
    # Sample data
    np.random.seed(42)
    dates = pd.date_range(start='2021-01-01', periods=100)
    sales_data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.poisson(300, 100),
        'Inventory': np.random.poisson(200, 100)
    })
    
    # Functions to calculate KPIs
    def calculate_kpis(sales_multiplier, inventory_multiplier):
        total_sales = sales_data['Sales'].sum() * sales_multiplier
        total_inventory = sales_data['Inventory'].sum() * inventory_multiplier
        return total_sales, total_inventory
    
    # Functions to create charts
    def create_sales_chart(sales_multiplier):
        adjusted_sales = sales_data['Sales'] * sales_multiplier
        chart_data = sales_data.copy()
        chart_data['Adjusted Sales'] = adjusted_sales
        sales_chart = alt.Chart(chart_data).mark_line().encode(
            x='Date',
            y='Adjusted Sales'
        ).properties(
            title='Adjusted Sales Over Time',
            width=600,
            height=400
        )
        return sales_chart
    
    def create_inventory_chart(inventory_multiplier):
        adjusted_inventory = sales_data['Inventory'] * inventory_multiplier
        chart_data = sales_data.copy()
        chart_data['Adjusted Inventory'] = adjusted_inventory
        inventory_chart = alt.Chart(chart_data).mark_line().encode(
            x='Date',
            y='Adjusted Inventory'
        ).properties(
            title='Adjusted Inventory Over Time',
            width=600,
            height=400
        )
        return inventory_chart
    
    # Sidebar inputs
    st.sidebar.header("Inputs")
    sales_multiplier = st.sidebar.slider("Sales Multiplier", 0.5, 2.0, 1.0)
    inventory_multiplier = st.sidebar.slider("Inventory Multiplier", 0.5, 2.0, 1.0)
    
    # Main Dashboard
    st.title("Retail Analytics Dashboard")
    st.header("Key Performance Indicators (KPIs)")
    
    # Calculate and display KPIs
    total_sales, total_inventory = calculate_kpis(sales_multiplier, inventory_multiplier)
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Inventory", f"${total_inventory:,.2f}")
    
    # Display charts
    st.header("Sales and Inventory Charts")
    sales_chart = create_sales_chart(sales_multiplier)
    inventory_chart = create_inventory_chart(inventory_multiplier)
    
    st.altair_chart(sales_chart)
    st.altair_chart(inventory_chart)
    
    # Scenario Modeling
    st.header("Scenario Modeling")
    st.write("Adjust the inputs in the sidebar to see how the changes affect sales and inventory.")
    
    # # Button to execute requests
    # if st.button("Execute Scenario"):
    #     st.write("Scenario Executed! The charts and KPIs are updated based on the inputs.")


with tab5:
    st.title("Retail Analytics Dashboard")
    st.header("Introduction to the Tool")
    st.write("""
        This Retail Analytics Dashboard provides valuable insights into sales and inventory management.
        Using this tool, retailers can:
        - Forecast sales and inventory needs
        - Optimize stock levels
        - Improve demand planning
        - Analyze sales trends
        - Segment customers
        - Optimize pricing strategies
        By leveraging these analytics, businesses can make informed decisions and enhance overall efficiency.
    """)

with tab6:
    st.title("Tool Usage Instructions")
    st.header("How to Use This Tool")
    st.write("""
        **Step 1: Adjust the Inputs**
        Use the sliders in the sidebar to adjust the sales and inventory multipliers. This allows you to model different scenarios and see how changes in sales and inventory levels affect key performance indicators (KPIs) and charts.
        
        **Step 2: Review KPIs**
        The KPIs section displays the total sales and total inventory based on the adjusted multipliers. This helps you quickly assess the impact of your input changes.
        
        **Step 3: Analyze Charts**
        The sales and inventory charts visualize the adjusted values over time. These charts help you understand trends and patterns in your data.
        
        **Step 4: Execute Scenario**
        Click the "Execute Scenario" button to apply the changes and update the charts and KPIs. This simulates executing a scenario based on your inputs.
        
        **Step 5: Explore Further**
        Use the insights gained from the dashboard to make data-driven decisions, optimize operations, and plan future strategies.
    """)

with tab7:
    st.title("Scenario Modeling")
    st.header("Interactive Model")

    # Sidebar inputs
    # st.sidebar.header("Adjust Inputs")
    # sales_multiplier = st.sidebar.slider("Sales Multiplier", 0.5, 2.0, 1.0)
    # inventory_multiplier = st.sidebar.slider("Inventory Multiplier", 0.5, 2.0, 1.0)
    
    # Main view
    st.subheader("Key Performance Indicators (KPIs)")

    # Calculate and display KPIs
    total_sales, total_inventory = calculate_kpis(sales_multiplier, inventory_multiplier)
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Total Inventory", f"${total_inventory:,.2f}")

    # Display charts
    st.subheader("Sales and Inventory Charts")
    sales_chart = create_sales_chart(sales_multiplier)
    inventory_chart = create_inventory_chart(inventory_multiplier)

    st.altair_chart(sales_chart)
    st.altair_chart(inventory_chart)

    # Button to execute requests
    if st.button("Execute Scenario"):
        st.write("Scenario Executed! The charts and KPIs are updated based on the inputs.")
    
    # Footer
    st.write("For further inquiries or collaboration, please contact us at [email@example.com](mailto:email@example.com).")

    