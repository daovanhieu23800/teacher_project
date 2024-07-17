import io
import json
import joblib
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from demand_forecasting import DemandForecasting


model = joblib.load("models/item_demand_forcast_lgb.pkl") 
app = FastAPI()


@app.post("/") 
async def api(request: Request):
    # print(request)
    form_data = await request.form()
    # print(form_data, type(form_data))
    uploaded_file = form_data.getlist("file")
    dict_data = {
        'id': form_data.getlist("id"), 
        'date': form_data.getlist("date"), 
        'store': form_data.getlist("store"), 
        'item': form_data.getlist("item")
    }
    # print(uploaded_file)
    try:
        # print(dict_data)
        # Handle file upload
        if uploaded_file:
            input_model_data = None
            file_extension = uploaded_file.filename.split('.')[-1]
            file_contents = await uploaded_file.read()
            if file_extension == "csv":
                input_model_data = pd.read_csv(io.BytesIO(file_contents), index_col=False)
            elif file_extension in ["xls", "xlsx"]:
                input_model_data = pd.read_excel(io.BytesIO(file_contents), index_col=False)
            else:
                return Response(content="Invalid file format. Only CSV and Excel files are supported.", status_code=400)
            
            output_json_string = DemandForecasting(model, input_model_data)
            return Response(content=output_json_string)

        # If no file is provided, check if the request body is JSON
        elif dict_data:
            try:
                input_model_data = pd.DataFrame(dict_data)
                # print(input_model_data)
                # print(model)
                output_json_string = DemandForecasting(model, input_model_data)
                return Response(content=output_json_string)
                
            except json.decoder.JSONDecodeError:
                # JSON decoding failed, not a JSON request
                raise HTTPException(status_code=400, detail="Invalid JSON input")
    except Exception as e:
        # If the input is neither a file nor valid JSON
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")