import streamlit as st
import pandas as pd
import numpy as np

def calculate_carbon(distance, vehicle_type):
    if vehicle_type == "EV":
        return distance * 0.03
    else:
        return distance * 0.22

def get_color(score):
    if score >= 80:
        return "green"
    elif score >= 60:
        return "yellow"
    else:
        return "red"

def render():
    st.title("Sustainability Score Summary")
    if "routes_df" not in st.session_state:
        st.warning("Please upload routes data on the Data Upload page.")
        return
    routes_df = st.session_state["routes_df"].copy()
    if "predicted_waste" in st.session_state:
        mean_waste = st.session_state["predicted_waste"].mean()
    else:
        mean_waste = 10  # fallback dummy value
    routes_df["carbon_score"] = routes_df.apply(lambda r: calculate_carbon(r["distance_km"], r["vehicle_type"]), axis=1)
    routes_df["predicted_waste"] = mean_waste
    routes_df["sustainability_score"] = 100 - (routes_df["carbon_score"] * 5 + routes_df["predicted_waste"] * 3)
    st.subheader("Sustainability Scores by Route")
    def color_score(val):
        color = get_color(val)
        return f"background-color: {color}"
    display_cols = ["route_id", "source", "destination", "distance_km", "vehicle_type", "carbon_score", "predicted_waste", "sustainability_score"]
    styled_df = routes_df[display_cols].copy()
    st.dataframe(styled_df.style.applymap(color_score, subset=["sustainability_score"]))
    # Download button
    csv = routes_df.to_csv(index=False)
    st.download_button("Download Sustainability Report", csv, "sustainability_report.csv", "text/csv") 