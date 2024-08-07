import pandas as pd
import numpy as np


def process(data: pd.DataFrame) -> pd.DataFrame:
    data['date'] = pd.to_datetime(data['date'])
    data['month'] = data['date'].dt.month
    data['day'] = data['date'].dt.dayofweek
    data['year'] = data['date'].dt.year

    return data


def DemandForecasting(model, input_data: pd.DataFrame):
    processed_input_data = process(input_data)
    # print(processed_input_data)
    cols = [i for i in processed_input_data.columns if i not in ['date','id']]
    input_data_for_model = processed_input_data[cols]
    input_data_for_model['store'] = pd.to_numeric(input_data_for_model['store'])
    input_data_for_model['item'] = pd.to_numeric(input_data_for_model['item'])
    # print(input_data_for_model)
    predictions = model.predict(input_data_for_model)
    
    # print(predictions)

    output_df = pd.DataFrame({
        "date": pd.to_datetime(input_data['date']),
        "sales": np.round(predictions).astype(int)
    })
    # print(output_df)
    return output_df