import io

import joblib
import pandas as pd
import lightgbm 
from fastapi import FastAPI, File
from pydantic import BaseModel
from starlette.responses import Response

from data_processing import process


forecast_model = joblib.load("./models/item_demand_forecast_lgb.pkl") 

app = FastAPI()

@app.get("/demand-forecasting") 
async def forecastAPI(file: bytes = File(...)):

    file_extension = file.filename.split(".")[-1]
    if file_extension == "csv":
        input_data = pd.read_csv(io.BytesIO(file), index_col=False, parse_dates=['date'])
    elif file_extension in ["xls", "xlsx"]:
        input_data = pd.read_excel(io.BytesIO(file), index_col=False, parse_dates=['date'])
    else:
        return Response(content="Invalid file format. Only CSV and Excel files are supported.", status_code=400)
    
    historical_data = pd.read_csv('./sample-data/historical_data.csv', index_col=False, parse_dates=["date"])
    processed_input_data = process(historical_data, input_data)
    cols = [col for col in processed_input_data.columns if col not in ['date', 'id', "sales", "year"]]
    input_data_for_model = processed_input_data[cols]

    # Use the model to make predictions
    predictions = forecast_model.predict(processed_input_data)

    output_data = pd.DataFrame({
        "sales":processed_input_data.predict(input_data_for_model)
    })
    return Response(content=output_data, media_type="text/plain")
