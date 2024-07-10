import io

import requests
from PIL import Image
import pandas as pd
import streamlit as st
from requests_toolbelt.multipart.encoder import MultipartEncoder


# interact with FastAPI endpoint
backend = "http://fastapi:8000/demand-forecasting"


def process(data, server_url: str):

    m = MultipartEncoder(fields={"file": ("filename", data, "csv/xls/xlsx")})

    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
    )

    return r


# construct UI layout
st.title("Store Items Demand Forecasting")

st.write(
    """Forecast the demand for store items using a LightGBM model.
         This streamlit example uses a FastAPI service as backend.
         Visit this URL at `:8000/docs` for FastAPI documentation."""
)  # description and instructions

st.markdown("### Historical data")
st.dataframe(pd.read_csv('./sample-data/train.csv', index_col=False))  # sample data

input_data = st.file_uploader("insert tabula data", type=['csv', 'xls', 'xlsx'])  # data upload widget

if st.button("Get forecasting results"):

    col1, col2 = st.columns(2)

    if input_data:
        output_data = process(input_data, backend)
        col1.markdown("### Input data")
        col1.dataframe(input_data)

        col2.markdown("### Next 3 months of store item sales")
        col2.dataframe(output_data)

    else:
        # handle case with no data
        st.write("Insert data!")
