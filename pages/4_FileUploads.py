import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Data Upload", page_icon="📈", layout="wide")

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
st.title("Data Uploads Page")

# Define dataset types and their corresponding labels
dataset_types = {
    'Sales Data': 'sales_data',
    'Inventory Data': 'inventory_data',
    'Customer Data': 'customer_data',
    'Product Data': 'product_data',
    'Supply Chain Data': 'supply_chain_data',
    'Marketing Data': 'marketing_data',
    'Online Retail Data': 'online_retail_data',
    'External Data': 'external_data',
    'Operational Data': 'operational_data'
}

# Initialize session state to store uploaded files if not already initialized
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = {dataset: None for dataset in dataset_types.values()}



# Add content to each column
col1, col2 ,col3 = st.columns((30,5,65))

with col1:
    st.write("Add your data here to be used within the app")
    # Add more content here
    # Create file uploaders for each dataset type
    for label, key in dataset_types.items():
        st.header(f"Upload Your {label}")
        uploaded_file = st.file_uploader(f"Choose a file for {label}", type=["csv", "xlsx"], key=key)
    
        if uploaded_file:
            if uploaded_file.type == "text/csv":
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.session_state.uploaded_files[key] = df
    
            # Display a preview of the uploaded data
            st.write(f"## Data Preview for {label}")
            st.dataframe(df.head())
    
            # Display a message confirming the file upload
            st.success(f"{label} uploaded successfully!")
with col2:
    st.write("")

with col3:
    # st.write("Column 2")
    # # Function to show the currently uploaded datasets
    def show_uploaded_datasets():
        st.header("Currently Uploaded Datasets")
        for label, key in dataset_types.items():
            if st.session_state.uploaded_files[key] is not None:
                st.write(f"#### {label}")
                st.dataframe(st.session_state.uploaded_files[key].head())
            else:
                st.write(f"#### {label} - No file uploaded")
    show_uploaded_datasets()








