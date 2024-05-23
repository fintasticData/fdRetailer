import requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image
import pandas as pd

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")
# Add your logo at the top of the page
st.image("fdLogo.png") # Adjust the width as needed

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>", unsafe_allow_html=True)


local_css("C:/MyPy/Streamlit/fdRetail/pages/style/style/style.css")

# ---- LOAD ASSETS ----
lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")
img_contact_form = Image.open("C:/MyPy/Streamlit/fdRetail/pages/images/yt_contact_form.png")
img_lottie_animation = Image.open("C:/MyPy/Streamlit/fdRetail/pages/images/yt_lottie_animation.png")

# ---- HEADER SECTION ----
with st.container():
    st.subheader("Hi, We are Fintastic Data :wave:")
    st.title("We are a data science team providing applications for industry")
    st.write(
        "We are passionate about finding ways to use Data Science in various industries."
    )
    st.write("[Learn More >](https://fintasticdata.com)")




if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Name:", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.session_state["my_input"] = my_input
    st.write("You have entered: ", my_input)
    
# Title of the app
st.title("CSV File Uploader")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file is uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Apply styling to the DataFrame
    styled_df = df.style\
        .highlight_max(axis=0, color='lightgreen')\
        .highlight_min(axis=0, color='lightcoral')\
        .set_properties(**{
            'background-color': 'whitesmoke',
            'color': 'black',
            'border-color': 'red'
        })\
        .set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', 'lightred'), ('color', 'white'), ('font-weight', 'bold')]}
        ])
    
    # Display the styled DataFrame
    st.write("DataFrame Preview:")
    st.dataframe(styled_df)
else:
    st.write("No file uploaded yet.")