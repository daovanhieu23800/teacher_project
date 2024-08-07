import io
import json
import base64

import joblib
import pandas as pd
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response
from dateutil.relativedelta import relativedelta

from demand_forecasting import DemandForecasting


model1 = joblib.load("models/item_demand_forcast_lgb_1month.pkl") 
model2 = joblib.load("models/item_demand_forcast_lgb_2month.pkl")
model3 = joblib.load("models/item_demand_forcast_lgb_3month.pkl")
app = FastAPI()


def process(model_list, input_data: pd.DataFrame):
    concat_df = pd.DataFrame()
    for i, model in enumerate(model_list):
        output = DemandForecasting(model, input_data)
        output['date'] = output['date'].apply(lambda date: date + relativedelta(months = i + 1))
        output['date'] = output['date'].dt.strftime('%Y-%m-%d')
        output = output.rename(columns={'date': f'{i+1}-month', 
                                        'sales': f'next {i+1}-month sales'})
        concat_df = pd.concat([concat_df, output], axis=1)
    
    # print(concat_df)
    json_string = concat_df.to_json(orient='records', indent=4)
    return json_string
    


@app.post("/") 
async def api(request: Request):
    # print(request)
    form_data = await request.form()
    # print(form_data.keys(), type(form_data))
    # print(f'file: {uploaded_file}')
    try:
        # print(dict_data)
        # Handle file upload
        if 'file' in form_data.keys():
            file_contents = base64.b64decode(form_data.getlist("file")[0])
            file_extension = form_data.getlist("file_ext")[0]
            # print(len(file_contents))
            input_model_data = None
            if file_extension == "csv":
                input_model_data = pd.read_csv(io.BytesIO(file_contents), index_col=False)
            elif file_extension in ["xls", "xlsx"]:
                input_model_data = pd.read_excel(io.BytesIO(file_contents), index_col=False)
            else:
                return Response(content="Invalid file format. Only CSV and Excel files are supported.", status_code=400)
            
            output_json_string = process([model1, model2, model3], input_model_data)
            return Response(content=output_json_string)

        # If no file is provided, check if the request body is JSON
        else:
            try:
                dict_data = {
                    'id': form_data.getlist("id"), 
                    'date': form_data.getlist("date"), 
                    'store': form_data.getlist("store"), 
                    'item': form_data.getlist("item")
                }
                input_model_data = pd.DataFrame(dict_data, index=[0])
                # print(input_model_data)
                # print(model)
                output_json_string = process([model1, model2, model3], input_model_data)
                return output_json_string
                # return Response(content=output_json_string)
                
            except json.decoder.JSONDecodeError:
                # JSON decoding failed, not a JSON request
                raise HTTPException(status_code=400, detail="Invalid JSON input")
    except Exception as e:
        # If the input is neither a file nor valid JSON
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    

 # For debugging purposes
if __name__ == "__main__":
    api()