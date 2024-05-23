import pickle
from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="21 Retail Forecasting Services", layout="wide")
st.image("fdLogo.png")

# # --- USER AUTHENTICATION ---
# import yaml
# from yaml.loader import SafeLoader

# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['pre-authorized']
# )
        
# authenticator.logout("Logout", "sidebar")
# name, authentication_status, username = authenticator.login()
authentication_status = True
if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    current_time  = date.today()
    # st.write(f"Welcome {name}")
    st.write(current_time)
    
    st.title("21 Retail Forecasting Services")
    st.write("Welcome to our Retail Forecasting Services platform. Our goal is to provide your retail business with the tools and insights needed to thrive in a competitive market.")
 
    # About Our Services
    with st.container():
        st.write("---")
        st.header("About Our Services")
        st.write(
            """
            We offer advanced retail forecasting services using cutting-edge machine learning techniques. Our services are designed to help retail businesses:
            
            - **Accurately predict future sales trends.**
            - **Optimize inventory management.**
            - **Improve demand forecasting.**
            - **Enhance decision-making with data-driven insights.**
 
            Our solutions leverage the latest advancements in machine learning to deliver reliable and actionable forecasts, ensuring you stay ahead in the competitive retail market.
            """
        )
 
    # Why Choose Us
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        
        with left_column:
            st.header("Why Choose Us")
            st.write(
                """
                By choosing our services, you benefit from:
                
                - **Expertise in Machine Learning and Data Science:** Our team consists of seasoned professionals with extensive experience in the field.
                - **Customized Forecasting Models:** Tailored to your specific business needs and goals.
                - **Real-Time Analytics and Reporting:** Stay updated with the latest trends and insights.
                - **Dedicated Support and Consultation:** We're here to help you every step of the way.
 
                Let us help you transform your retail operations with precise and insightful forecasting, enabling you to make informed decisions and drive growth.
                """
            )
        
        with right_column:
            st.header("Our Services")
            st.write(
                """
                We offer a range of services to meet your retail forecasting needs:
                
                - **Sales Trend Analysis:** Identify patterns and trends in your sales data to make informed predictions.
                - **Inventory Optimization:** Ensure optimal stock levels to meet demand without overstocking.
                - **Demand Forecasting:** Predict future demand to streamline your supply chain operations.
                - **Price Optimization:** Use data-driven insights to set the best prices for your products.
                - **Customer Segmentation:** Understand your customer base and target them more effectively.
                """
            )
    with st.container():
        st.write("---")
        st.header("Services Details")
        left_column, right_column = st.columns(2)
        # Define service descriptions
        services = {
            "Sales Trend Analysis": {
                "description": """
                **Sales Trend Analysis** helps you identify patterns and trends in your sales data to make informed predictions. By analyzing historical sales data, we can uncover seasonal trends, growth patterns, and potential opportunities for your business.
                
                **Benefits**:
                - Identify peak sales periods and plan promotions accordingly.
                - Understand product lifecycle trends to optimize inventory.
                - Gain insights into customer purchasing behaviors.
                """
            },
            "Inventory Optimization": {
                "description": """
                **Inventory Optimization** ensures that you maintain optimal stock levels to meet demand without overstocking. Using advanced algorithms, we help you balance inventory costs with service levels.
                
                **Benefits**:
                - Reduce excess inventory and associated carrying costs.
                - Minimize stockouts and improve customer satisfaction.
                - Optimize reorder points and quantities for efficient supply chain management.
                """
            },
            "Demand Forecasting": {
                "description": """
                **Demand Forecasting** predicts future demand to streamline your supply chain operations. By leveraging machine learning models, we provide accurate forecasts that help you plan production, manage inventory, and schedule deliveries.
                
                **Benefits**:
                - Improve supply chain efficiency and reduce operational costs.
                - Enhance accuracy in production planning and resource allocation.
                - Respond proactively to market changes and customer demand.
                """
            },
            "Price Optimization": {
                "description": """
                **Price Optimization** uses data-driven insights to set the best prices for your products. By analyzing market conditions, customer behavior, and competitor pricing, we help you find the optimal price points to maximize revenue and profitability.
                
                **Benefits**:
                - Increase sales and profit margins.
                - Respond dynamically to market changes.
                - Enhance customer satisfaction with competitive pricing.
                """
            },
            "Customer Segmentation": {
                "description": """
                **Customer Segmentation** helps you understand your customer base and target them more effectively. By segmenting customers based on their behaviors, preferences, and demographics, we enable personalized marketing strategies and improved customer experiences.
                
                **Benefits**:
                - Improve marketing campaign effectiveness.
                - Enhance customer loyalty and retention.
                - Identify high-value customer segments for targeted promotions.
                """
            }
        }
        
        # Interactive service selection
        service_selected = st.selectbox("Select a service to learn more:", list(services.keys()))
        
        # Display the selected service's details
     
        st.header(service_selected)
        st.write(services[service_selected]["description"])
 
 
    # Call to Action
    st.write("---")
    st.header("Get Started")
    st.write("Ready to take your retail forecasting to the next level? Contact us today to learn more about our services and how we can help your business thrive.")
    st.button("Learn More", on_click=lambda: st.write("Visit [our website](http://www.fintasticdata.com) for more information."))
 
    # Footer
    st.write("---")
    st.write("[Learn More >](http://www.fintasticdata.com)")
 
