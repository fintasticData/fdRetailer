import streamlit as st
import pandas as pd
from datetime import datetime

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

# Define dataset types
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
    st.session_state.uploaded_files = {value: None for value in dataset_types.values()}
if 'temp_uploaded_file' not in st.session_state:
    st.session_state.temp_uploaded_file = None

# Function to get file size
def get_file_size(file):
    file.seek(0, 2)  # Move to the end of the file
    size = file.tell()  # Get the current position, which is the file size
    file.seek(0)  # Reset the file position to the beginning
    return size

# Upload widget
st.write("## Upload Your Dataset")
dataset_type = st.selectbox("Select Dataset Type", list(dataset_types.keys()))
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file:
    st.session_state.temp_uploaded_file = {
        'file': uploaded_file,
        'dataset_type': dataset_type,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if st.session_state.temp_uploaded_file:
    st.write(f"Selected File: {st.session_state.temp_uploaded_file['file'].name}")
    if st.button("Commit File"):
        temp_file_info = st.session_state.temp_uploaded_file
        key = dataset_types[temp_file_info['dataset_type']]
        file = temp_file_info['file']
        if file.type == "text/csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.session_state.uploaded_files[key] = {
            'file_name': file.name,
            'data': df,
            'file_size': get_file_size(file),
            'rows': len(df),
            'timestamp': temp_file_info['timestamp']
        }
        st.session_state.temp_uploaded_file = None
        st.success(f"{file.name} uploaded successfully!")

# Summary Table
st.write("### Summary of Uploaded Files")
summary_data = []
for label, key in dataset_types.items():
    if st.session_state.uploaded_files[key] is not None:
        file_info = st.session_state.uploaded_files[key]
        if 'timestamp' not in file_info:
            file_info['timestamp'] = "N/A"
        summary_data.append({
            "Dataset": label,
            "File Name": file_info['file_name'],
            "Rows": file_info['rows'],
            "File Size (KB)": f"{file_info['file_size'] / 1024:.2f}",
            "Date Time Added": file_info['timestamp']
        })

if summary_data:
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary)
else:
    st.write("No files uploaded yet.")

# View Dataset Section
st.write("## View Uploaded Dataset")
view_dataset_type = st.selectbox("Select Dataset Type to View", list(dataset_types.keys()), key="view_dataset")

if view_dataset_type:
    key = dataset_types[view_dataset_type]
    if st.session_state.uploaded_files[key] is not None:
        st.write(f"### Data Preview for {view_dataset_type}")
        st.dataframe(st.session_state.uploaded_files[key]['data'].head())
    else:
        st.write(f"No data available for {view_dataset_type}.")
