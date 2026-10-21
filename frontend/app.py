import streamlit as st
import pandas as pd
import requests

BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Revenue Prediction")
st.write("Predict the total sales revenue of a product in a specific store.")
st.subheader("Online Prediction")

product_weight = st.number_input("Product Weight", min_value=0.0, value=12.5)
product_allocated_area = st.number_input("Product Allocated Area (Ratio)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
product_mrp = st.number_input("Product MRP ($)", min_value=0.0, value=150.0)
store_establishment_year = st.number_input("Store Establishment Year", min_value=1900, max_value=2025, value=2009)

product_sugar_content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
product_type = st.selectbox("Product Type", [
    "Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy", "Household",
    "Baking Goods", "Canned", "Health and Hygiene", "Meat", "Soft Drinks",
    "Breads", "Hard Drinks", "Others", "Starchy Foods", "Breakfast", "Seafood"
])
store_size = st.selectbox("Store Size", ["Medium", "High", "Small"])
store_location_city_type = st.selectbox("Store Location City Type", ["Tier 2", "Tier 1", "Tier 3"])
store_type = st.selectbox("Store Type", ["Supermarket Type2", "Supermarket Type1", "Departmental Store", "Food Mart"])

if st.button("Predict", type="primary"):
    payload = {
        "Product_Weight": product_weight,
        "Product_Allocated_Area": product_allocated_area,
        "Product_MRP": product_mrp,
        "Store_Establishment_Year": store_establishment_year,
        "Product_Sugar_Content": product_sugar_content,
        "Product_Type": product_type,
        "Store_Size": store_size,
        "Store_Location_City_Type": store_location_city_type,
        "Store_Type": store_type
    }
    
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=payload)
    
    if response.status_code == 200:
        prediction = response.json()['Predicted Sales Revenue']
        st.success(f"Predicted Sales Revenue: ${prediction:,.2f}")
    else:
        st.error("Unable to connect to the prediction API. Please check the backend.")


st.subheader("Batch Prediction")

uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})
        
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed successfully!")
            st.write(predictions)
        else:
            st.error("Unable to connect to the prediction API.")
