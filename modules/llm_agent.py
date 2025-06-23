import os
import pandas as pd
import streamlit as st
import requests

def summarize_data(inventory_df, routes_df):
    # Total predicted waste
    total_predicted_waste = inventory_df["predicted_waste"].sum() if "predicted_waste" in inventory_df else None
    # Top 2 most waste-prone products
    if "predicted_waste" in inventory_df:
        top_waste = inventory_df.sort_values("predicted_waste", ascending=False).head(2)
        top_products = top_waste[["product_id", "category", "predicted_waste"]].to_dict(orient="records")
    else:
        top_products = []
    # Total emissions per route
    if "carbon_score" in routes_df:
        emissions = routes_df.groupby(["route_id", "vehicle_type"])["carbon_score"].sum().reset_index()
    else:
        emissions = pd.DataFrame()
    # Vehicle type suggestions (prefer EV if available)
    vehicle_suggestions = []
    if not routes_df.empty:
        for _, row in routes_df.iterrows():
            if row.get("vehicle_type") == "Diesel":
                vehicle_suggestions.append(f"Consider switching route {row['route_id']} to EV if possible.")
    return total_predicted_waste, emissions, vehicle_suggestions, top_products

def build_prompt(total_predicted_waste, emissions, vehicle_suggestions, top_products):
    prompt = f"""
You are EcoRoute, an AI assistant helping Walmart reduce food waste and optimize supply chain sustainability. Based on the current inventory and delivery data below, suggest the best way to reduce spoilage and carbon emissions.

Data Summary:
- Total predicted waste: {total_predicted_waste}
- Total emissions per route:
{emissions.to_string(index=False) if not emissions.empty else 'N/A'}
- Vehicle type suggestions:
{chr(10).join(vehicle_suggestions) if vehicle_suggestions else 'N/A'}
- Top 2 most waste-prone products:
{chr(10).join([f"Product {p['product_id']} ({p['category']}): {p['predicted_waste']:.2f}%" for p in top_products]) if top_products else 'N/A'}

Please provide actionable, easy-to-read sustainability tips personalized to this data.
"""
    return prompt

def get_sustainability_advice(inventory_df, routes_df):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key not found. Please set it in your .env file or as an environment variable."
    total_predicted_waste, emissions, vehicle_suggestions, top_products = summarize_data(inventory_df, routes_df)
    prompt = build_prompt(total_predicted_waste, emissions, vehicle_suggestions, top_products)
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(f"{url}?key={api_key}", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return f"Error communicating with Gemini: {e}" 