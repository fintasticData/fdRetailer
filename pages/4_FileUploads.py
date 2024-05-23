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

# Function to get file size
def get_file_size(file):
    file.seek(0, 2)  # Move to the end of the file
    size = file.tell()  # Get the current position, which is the file size
    file.seek(0)  # Reset the file position to the beginning
    return size

# Create a two-column layout
col1, col2 = st.columns([3, 2])

with col1:
    for label, key in dataset_types.items():
        with st.container():
            st.markdown(
                """
                <style>
                .data-row {
                    border: 1px solid #ddd;
                    padding: 10px;
                    margin-bottom: 10px;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
            st.write(f"**{label}**")
            if st.session_state.uploaded_files[key] is not None:
                file_info = st.session_state.uploaded_files[key]
                st.write(file_info['file_name'])
                st.write(f"Session State Key: {key}")
            else:
                if st.button(f"Upload {label}", key=f"upload_{key}"):
                    # Store the fact that we are in upload mode for this key
                    st.session_state[f"upload_mode_{key}"] = True

            if st.session_state.uploaded_files[key] is not None:
                cols = st.columns([3, 1, 1, 1])
                with cols[0]:
                    st.success("✔️ Uploaded")
                with cols[1]:
                    st.write(st.session_state.uploaded_files[key]['rows'])
                with cols[2]:
                    st.write(f"{st.session_state.uploaded_files[key]['file_size'] / 1024:.2f} KB")
                with cols[3]:
                    if st.button(f"View {label}", key=f"view_{key}"):
                        st.session_state['view_data'] = st.session_state.uploaded_files[key]['data']
                        st.session_state['view_label'] = label
            else:
                st.write("➕ Not Uploaded")

            # Handle the file uploader
            if st.session_state.get(f"upload_mode_{key}", False):
                uploaded_file = st.file_uploader(f"Choose a file for {label}", type=["csv", "xlsx"], key=f"file_uploader_{key}")
                if uploaded_file is not None:
                    if uploaded_file.type == "text/csv":
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)

                    st.session_state.uploaded_files[key] = {
                        'file_name': uploaded_file.name,
                        'data': df,
                        'file_size': get_file_size(uploaded_file),
                        'rows': len(df)
                    }
                    st.session_state[f"upload_mode_{key}"] = False
                    st.experimental_rerun()

with col2:
    if 'view_data' in st.session_state:
        st.write(f"### Data Preview for {st.session_state['view_label']}")
        st.dataframe(st.session_state['view_data'].head())
