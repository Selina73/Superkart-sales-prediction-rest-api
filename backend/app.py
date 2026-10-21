import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

superkart_sales_api = Flask("SuperKart Sales Predictor")

model = joblib.load("SuperKart_revenue_forecast_model_v1_0.joblib")

@superkart_sales_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Sales Prediction API!"

@superkart_sales_api.post('/v1/sales')
def predict_sales():
    """
    This function handles POST requests to the '/v1/sales' endpoint.
    It expects a JSON payload containing product/store details and returns
    the predicted sales revenue as a JSON response.
    """
    data = request.get_json()

    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Establishment_Year': data['Store_Establishment_Year'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Type': data['Product_Type'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type']
    }

    input_data = pd.DataFrame([sample])

    predicted_sales = model.predict(input_data)[0]

    predicted_sales = round(float(predicted_sales), 2)

    return jsonify({'Predicted Sales Revenue': predicted_sales})


@superkart_sales_api.post('/v1/salesbatch')
def predict_sales_batch():
    """
    This function handles POST requests to the '/v1/salesbatch' endpoint.
    It expects a CSV/Excel file containing details for multiple records
    and returns the predicted sales revenues as a dictionary in the JSON response.
    """
    file = request.files['file']

    if file.filename.endswith('.csv'):
        input_data = pd.read_csv(file)
    else:
        input_data = pd.read_excel(file)

    predicted_sales = model.predict(input_data).tolist()

    predicted_sales_rounded = [round(float(sales), 2) for sales in predicted_sales]

    try:
        product_ids = input_data['Product_Id'].tolist()
        output_dict = dict(zip(product_ids, predicted_sales_rounded))
    except KeyError:
        output_dict = {"Predictions": predicted_sales_rounded}

    return output_dict

if __name__ == '__main__':
    superkart_sales_api.run(debug=True)
