import pickle
from pathlib import Path
import streamlit as st
import pandas as pd
# from st_pages import Page, Section, add_page_title, show_pages
# import streamlit_authenticator as stauth
# from streamlit_authenticator.utilities.hasher import Hasher
from datetime import date


st.set_page_config(page_title="21 Retail Forecasting Services", layout="wide")
st.image("fdLogo.png")

# Custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles.css")



# Main Content
st.markdown("""
<div class="container">
    <h1>21 Retail Forecasting Services</h1>
    <p>Welcome to our Retail Forecasting Services platform. Our goal is to provide your retail business with the tools and insights needed to thrive in a competitive market.</p>
    <div class="flex-container">
        <div class="flex-item">
            <div class="card">
                <h2>About Our Services</h2>
                <p>We offer advanced retail forecasting services using cutting-edge machine learning techniques. Our services are designed to help retail businesses:</p>
                <ul>
                    <li>Accurately predict future sales trends.</li>
                    <li>Optimize inventory management.</li>
                    <li>Improve demand forecasting.</li>
                    <li>Enhance decision-making with data-driven insights.</li>
                </ul>
                <p>Our solutions leverage the latest advancements in machine learning to deliver reliable and actionable forecasts, ensuring you stay ahead in the competitive retail market.</p>
            </div>
        </div>
        <div class="flex-item">
            <div class="card">
                <h2>Why Choose Us</h2>
                <p>By choosing our services, you benefit from:</p>
                <ul>
                    <li>Expertise in Machine Learning and Data Science: Our team consists of seasoned professionals with extensive experience in the field.</li>
                    <li>Customized Forecasting Models: Tailored to your specific business needs and goals.</li>
                    <li>Real-Time Analytics and Reporting: Stay updated with the latest trends and insights.</li>
                    <li>Dedicated Support and Consultation: We’re here to help you every step of the way.</li>
                </ul>
                <p>Let us help you transform your retail operations with precise and insightful forecasting, enabling you to make informed decisions and drive growth.</p>
            </div>
        </div>
    </div>
    <div class="card">
        <h2>Our Services</h2>
        <ul>
            <li>Sales Trend Analysis: Identify patterns and trends in your sales data to make informed predictions.</li>
            <li>Inventory Optimization: Ensure optimal stock levels to meet demand without overstocking.</li>
            <li>Demand Forecasting: Predict future demand to streamline your supply chain operations.</li>
            <li>Price Optimization: Use data-driven insights to set the best prices for your products.</li>
            <li>Customer Segmentation: Understand your customer base and target them more effectively.</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Page Footer
st.markdown("""
<footer>
    <p>&copy; 2024 Future Forecaster. All rights reserved.</p>
</footer>
""", unsafe_allow_html=True)
