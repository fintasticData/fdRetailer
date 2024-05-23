import streamlit as st

# Define services data
services = [
    {
        "title": "Retail Forecasting",
        "description": "Accurately predict future sales trends using advanced machine learning techniques.",
        "features": ["Advanced ML models", "Historical data analysis", "Seasonal trend identification"],
        "benefits": ["Increase sales accuracy", "Optimize stock levels", "Improve customer satisfaction"],
        "cta": "Learn More"
    },
    {
        "title": "Inventory Optimization",
        "description": "Optimize your inventory management to reduce costs and prevent stockouts.",
        "features": ["Real-time tracking", "Predictive analytics", "Automated replenishment"],
        "benefits": ["Reduce holding costs", "Minimize stockouts", "Improve cash flow"],
        "cta": "Get Started"
    },
    {
        "title": "Demand Forecasting",
        "description": "Improve demand forecasting to ensure you meet customer needs effectively.",
        "features": ["Demand sensing", "Market analysis", "Sales pattern recognition"],
        "benefits": ["Better demand planning", "Reduce surplus inventory", "Increase operational efficiency"],
        "cta": "Contact Us"
    },
    {
        "title": "Sales Analysis",
        "description": "Gain insights into your sales performance with comprehensive data analysis.",
        "features": ["Detailed reporting", "Custom dashboards", "Trend analysis"],
        "benefits": ["Identify growth opportunities", "Improve sales strategies", "Make data-driven decisions"],
        "cta": "Explore Now"
    },
    {
        "title": "Customer Segmentation",
        "description": "Segment your customers to tailor marketing strategies.",
        "features": ["Behavioral analysis", "Demographic segmentation", "Customer profiling"],
        "benefits": ["Targeted marketing", "Personalized campaigns", "Enhanced customer engagement"],
        "cta": "Find Out More"
    },
    {
        "title": "Price Optimization",
        "description": "Optimize your pricing strategy for maximum profit.",
        "features": ["Dynamic pricing", "Competitor analysis", "Market demand estimation"],
        "benefits": ["Increased revenue", "Competitive edge", "Improved profit margins"],
        "cta": "Optimize Now"
    },
    {
        "title": "Churn Prediction",
        "description": "Predict and reduce customer churn using predictive analytics.",
        "features": ["Customer behavior analysis", "Churn modeling", "Retention strategies"],
        "benefits": ["Reduced churn rates", "Improved customer loyalty", "Increased lifetime value"],
        "cta": "Prevent Churn"
    },
    {
        "title": "Market Basket Analysis",
        "description": "Analyze purchase patterns to optimize product placement and cross-selling.",
        "features": ["Association rule learning", "Purchase pattern analysis", "Product recommendations"],
        "benefits": ["Increased sales", "Enhanced customer experience", "Better product placement"],
        "cta": "Analyze Now"
    },
    {
        "title": "Supply Chain Optimization",
        "description": "Optimize your supply chain for efficiency and cost reduction.",
        "features": ["Logistics planning", "Inventory management", "Supplier performance analysis"],
        "benefits": ["Reduced operational costs", "Improved efficiency", "Better supplier relationships"],
        "cta": "Optimize Supply Chain"
    },
]

# Page configuration
st.set_page_config(page_title="Our Products and Services", layout="wide")
st.image("fdLogo.png")

# Page title
st.title("Our Products and Services")

# Function to render a single service card
def render_service_card(service):
    st.markdown(f"""
        <div style='border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 20px; background-color: #fff;'>
            <h3 style='background-color: #333; color: #fff; padding: 10px; border-radius: 5px;'>{service['title']}</h3>
            <p>{service['description']}</p>
            <p><strong>✨ Features:</strong></p>
            <ul>
                {''.join([f"<li>{feature}</li>" for feature in service['features']])}
            </ul>
            <p><strong>💡 Benefits:</strong></p>
            <ul>
                {''.join([f"<li>{benefit}</li>" for benefit in service['benefits']])}
            </ul>
            <a href='#' style='display: inline-block; padding: 10px 20px; background-color: #ff4b4b; color: #fff; border-radius: 5px; text-decoration: none;'>{service['cta']}</a>
        </div>
    """, unsafe_allow_html=True)

# Render services in a 3x3 grid
cols = st.columns(3)
for i, service in enumerate(services):
    with cols[i % 3]:
        render_service_card(service)
