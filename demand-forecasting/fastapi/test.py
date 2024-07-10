import io

import joblib
import pandas as pd

from data_processing import process


forecast_model = joblib.load("./models/item_demand_forecast_lgb.pkl") 

historical_data = pd.read_csv('./sample-data/historical_data.csv', index_col=False, parse_dates=["date"])
input_data = pd.read_csv('./sample-data/test.csv', index_col=False, parse_dates=["date"])
processed_input_data = process(historical_data, input_data)
cols = [col for col in processed_input_data.columns if col not in ['date', 'id', "sales", "year"]]
input_data_for_model = processed_input_data[cols]

# Use the model to make predictions
predictions = forecast_model.predict(processed_input_data)

output_data = pd.DataFrame({
    "sales":processed_input_data.predict(input_data_for_model)
})

output_data.to_csv("output.csv", index=False)