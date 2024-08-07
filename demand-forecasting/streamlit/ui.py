import io
import json
import base64

import requests
import pandas as pd
import streamlit as st
from requests_toolbelt.multipart.encoder import MultipartEncoder


# interact with FastAPI endpoint
# for running FastAPI and Streamlit apps separately, use the following:
# backend = "http://0.0.0.0:8080/"
# for running docker, use the following:
backend = "http://fastapi:8080/"


def process(data, server_url: str):
    session = requests.Session()
    session.trust_env = False

    r = session.post(
        server_url, data=data, timeout=30000
    )

    # print(r)
    return r.json()


# construct UI layout
st.title("Store Items Demand Forecasting")

st.write(
    """Forecast the demand for store items using a LightGBM model.
         This streamlit example uses a FastAPI service as backend.
         Visit this URL at `:8000/docs` for FastAPI documentation."""
)  # description and instructions

st.markdown("### Historical data")
st.dataframe(pd.read_csv('data/train.csv', index_col=False))  # sample data

tab1, tab2 = st.tabs(["Input 1 Item", "Input many Items"])

with tab1:
    with st.form(key='filling_form'):
        datetime = st.date_input("Select date for forecasting", value=None)  # date input widget
        store_id = st.number_input("Enter store ID from the Historical Data above", value=None)  # store ID input widget
        item_id = st.number_input("Enter item ID from the Historical Data above", value=None)  # item ID input widget
        
        if st.form_submit_button("Get forecasting results"):
            try:
                if datetime is not None and store_id is not None and item_id is not None:
                    inserted_data = {
                        'id':0, 
                        'date':str(datetime), 
                        'store':int(store_id), 
                        'item':int(item_id)
                    }
                    col1, col2 = st.columns(2)
                    col1.markdown("### Input data")
                    col1.dataframe(pd.DataFrame([inserted_data]))
                    
                    # print(f'inserted_data: {inserted_data}')
                    output_data = json.loads(process(inserted_data, backend))
                    # print(output_data)
                    col2.markdown("### Predicted sales in next")
                    col2.dataframe(pd.DataFrame(output_data))
                else:
                    st.error('No input data to forecast. Please fill in the form above.')

            except Exception as e:
                st.error(e)        
        

with tab2:
    uploaded_file = st.file_uploader("Upload tabula data if you want to predict more than 1 item", type=['csv', 'xls', 'xlsx']) 

    if st.button("Get forecasting results"):
        try:
            if uploaded_file is not None:
                col1, col2 = st.columns(2)
                col1.markdown("### Input data")
                uploaded_file_ext = uploaded_file.name.split('.')[-1]
                uploaded_data = None
                if uploaded_file_ext in ["xls", "xlsx"]:
                    uploaded_data = pd.read_excel(io.BytesIO(uploaded_file.read()), index_col=False)
                else:
                    uploaded_data = pd.read_csv(io.BytesIO(uploaded_file.read()), index_col=False)
                
                col1.dataframe(uploaded_data)
                # print(type(uploaded_data.to_dict()))

                # Convert file content to base64
                encoded_file = base64.b64encode(uploaded_file.getvalue()).decode('utf-8')
                
                # Create JSON payload
                data = {
                    "file_ext": uploaded_file_ext,
                    "file": encoded_file
                }
                output_data = process(data, backend)
                col2.markdown("### Predicted sales in next")

                output_df = pd.DataFrame(output_data)
                col2.dataframe(output_df)

                st.download_button(
                    label="Download data as CSV",
                    data=output_df.to_csv(index=False).encode('utf-8'),
                    file_name='data.csv',
                    mime='text/csv',
                )
            else:
                st.error('No input data to forecast. Please upload data above.')
                
        except Exception as e:
            st.error(e)