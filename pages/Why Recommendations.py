import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="FMCG Recommendations", page_icon="🛒", layout="wide")

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

# Title of the page
st.title("FMCG Recommendations")

# Introduction
st.write("Fast-Moving Consumer Goods (FMCG) companies can leverage recommendation systems to improve customer experience and drive sales. Personalized recommendations, targeted marketing, and inventory management are some key areas where recommendation systems can make a significant impact.")

# Key Highlights
st.header("Key Highlights for FMCG Recommendations")

# Display highlights in columns using KPI widgets
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Personalized Recommendations", value="Increased Engagement")
    st.write("Provide personalized product recommendations based on customer behavior. This leads to higher engagement and customer satisfaction.")

with col2:
    st.metric(label="Targeted Marketing", value="Higher Conversion Rates")
    st.write("Target promotions and discounts based on customer purchase history. This can significantly increase conversion rates.")

with col3:
    st.metric(label="Inventory Management", value="Optimized Supply Chain")
    st.write("Use demand forecasting to optimize inventory levels and reduce costs. This ensures products are available when customers need them.")

# Another row of highlights
col4, col5, col6 = st.columns(3)
with col4:
    st.metric(label="Customer Engagement", value="Improved Satisfaction")
    st.write("Enhance user experience and loyalty through personalized recommendations. Satisfied customers are more likely to become repeat buyers.")

with col5:
    st.metric(label="Data-Driven Decision Making", value="Market Insights")
    st.write("Gain insights into market trends and customer preferences. Use this data to make informed decisions about product development and marketing strategies.")

with col6:
    st.metric(label="Competitive Advantage", value="Stay Ahead in the Market")
    st.write("Use recommendation systems to gain a competitive edge in the FMCG industry. By offering personalized recommendations, you can differentiate your brand from competitors.")

# Interesting Statistics
st.header("Interesting Statistics")

# Static bar chart example
st.subheader("Customer Purchase Behavior")
purchase_data = {
    'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
    'Sales': [2500, 1800, 3200, 1400, 2000]
}
purchase_df = pd.DataFrame(purchase_data)

fig = px.bar(purchase_df, x='Product', y='Sales', text='Sales', color='Sales', 
             color_continuous_scale=px.colors.sequential.Plasma)

fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# Static pie chart example
st.subheader("Customer Segmentation")
segment_data = {
    'Segment': ['Segment A', 'Segment B', 'Segment C', 'Segment D'],
    'Customers': [30, 25, 20, 25]
}
segment_df = pd.DataFrame(segment_data)

fig2 = px.pie(segment_df, names='Segment', values='Customers', title='Customer Segmentation',
              color_discrete_sequence=px.colors.sequential.RdBu)

st.plotly_chart(fig2, use_container_width=True)

# Footer with a call to action
st.write("---")
st.header("Implement Recommendations for Your FMCG Business")
st.write("Start implementing recommendation systems to enhance customer experience and drive sales in your FMCG business. Contact us to learn more about how we can help you implement these systems.")

# Footer link
st.write("---")
st.write("[Learn More >](https://yourfmcgcompany.com)")
