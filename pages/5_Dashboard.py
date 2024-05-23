import streamlit as st
import pandas as pd

import streamlit_shadcn_ui as ui
from local_components import card_container

# CONFIGS
YEAR = 2023
PREVIOUS_YEAR = 2022
CITIES = ["Tokyo", "Yokohama", "Osaka"]
DATA_URL = "https://raw.githubusercontent.com/Sven-Bo/datasets/master/store_sales_2022-2023.csv"
BAR_CHART_COLOR = "Grey"

st.set_page_config(page_title="Sales Dashboard", page_icon="📈")
# Add your logo at the top of the page
st.image("fdLogo.png") # Adjust the width as needed

st.title(f"Fintastic Sales Dashboard", anchor=False)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

@st.cache_data
def get_and_prepare_data(data):
    df = pd.read_csv(data).assign(
        date_of_sale=lambda df: pd.to_datetime(df["date_of_sale"]),
        month=lambda df: df["date_of_sale"].dt.month,
        year=lambda df: df["date_of_sale"].dt.year,
    )
    return df

df = get_and_prepare_data(data=DATA_URL)

# Calculate total revenue for each city and year, and then calculate the percentage change
city_revenues = (
    df.groupby(["city", "year"])["sales_amount"]
    .sum()
    .unstack()
    .assign(change=lambda x: x.pct_change(axis=1)[YEAR] * 100)
)

# Display the data for each city in separate columns
columns = st.columns(3)
for i, city in enumerate(CITIES):
    with columns[i]:
        ui.metric_card(
            title=city,
            content=f"$ {city_revenues.loc[city, YEAR]:,.2f}",
            description=f"vs. Last Year: {city_revenues.loc[city, 'change']:.2f}% change",
            key=f"card{i}",
        )

analysis_type = ui.tabs(
    options=["Month", "Product Category"],
    default_value="Month",
    key="analysis_type",
)

# Dropdown for selecting a city
selected_city = ui.select("Select a city:", CITIES)

# Toggle for selecting the year for visualization
previous_year_toggle = ui.switch(
    default_checked=False, label="Previous Year", key="switch_visualization"
)
visualization_year = PREVIOUS_YEAR if previous_year_toggle else YEAR
# Display the year above the chart based on the toggle switch
st.write(f"**Sales for {visualization_year}**")

# Filter data based on selection for visualization
if analysis_type == "Product Category":
    filtered_data = (
        df.query("city == @selected_city & year == @visualization_year")
        .groupby("product_category", dropna=False)["sales_amount"]
        .sum()
        .reset_index()
        .rename(columns={"product_category": "category"})
    )
else:
    # Group by month number
    filtered_data = (
        df.query("city == @selected_city & year == @visualization_year")
        .groupby("month", dropna=False)["sales_amount"]
        .sum()
        .reset_index()
        .rename(columns={"month": "category"})
    )
    # Ensure month column is formatted as two digits for consistency
    filtered_data["category"] = filtered_data["category"].apply(lambda x: f"{x:02d}")

# Vega-Lite specification with values on bars
vega_spec = {
    "data": {"values": filtered_data.to_dict("records")},
    "layer": [
        {
            "mark": {"type": "bar", "cornerRadiusEnd": 4},
            "encoding": {
                "x": {
                    "field": "category",
                    "type": "nominal",
                    "axis": {
                        "labelAngle": 0,
                        "title": None,
                        "grid": False,
                    },
                },
                "y": {
                    "field": "sales_amount",
                    "type": "quantitative",
                    "axis": {
                        "title": None,
                        "grid": False,
                    },
                },
                "color": {"value": BAR_CHART_COLOR},
            },
        },
        {
            "mark": {"type": "text", "align": "center", "baseline": "middle", "dy": -5},
            "encoding": {
                "x": {"field": "category", "type": "nominal"},
                "y": {"field": "sales_amount", "type": "quantitative"},
                "text": {"field": "sales_amount", "type": "quantitative"},
            },
        },
    ],
}

# Display the chart
with card_container(key="chart"):
    st.vega_lite_chart(vega_spec, use_container_width=True)


# Title of the app
st.title("CSV File Uploader")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame
    st.write("DataFrame Preview:")
    st.dataframe(df)
else:
    st.write("No file uploaded yet.")
