import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# Dummy model for prototype; replace with XGBoost or real model as needed
def train_dummy_model(df):
    X = df[["stock", "demand_forecast", "shelf_life"]]
    # Simulate waste as a function of overstock and shelf life
    y = np.clip((df["stock"] - df["demand_forecast"]) / (df["shelf_life"] + 1) * 10, 0, 100)
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    model.fit(X, y)
    return model

def render():
    st.title("Inventory Waste Prediction")
    if "inventory_df" not in st.session_state:
        st.warning("Please upload inventory data on the Data Upload page.")
        return
    df = st.session_state["inventory_df"].copy()
    model = train_dummy_model(df)
    X = df[["stock", "demand_forecast", "shelf_life"]]
    df["predicted_waste"] = model.predict(X)
    st.session_state["predicted_waste"] = df["predicted_waste"]
    st.subheader("Predicted Waste by Product")
    top_waste = df.sort_values("predicted_waste", ascending=False).head(10)
    st.bar_chart(top_waste.set_index("product_id")["predicted_waste"])
    st.dataframe(top_waste[["product_id", "category", "stock", "demand_forecast", "shelf_life", "predicted_waste"]]) 