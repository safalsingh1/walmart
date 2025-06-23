import streamlit as st
from modules import data_upload, waste_prediction, route_optimizer, sustainability_summary, llm_agent
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="EcoRoute: AI-Driven Sustainable Supply Chain Optimization", layout="wide")

PAGES = {
    "1. Data Upload": data_upload,
    "2. Waste Prediction": waste_prediction,
    "3. Route Optimizer": route_optimizer,
    "4. Sustainability Summary": sustainability_summary
}

st.sidebar.title("EcoRoute Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# EcoRoute Assistant Sidebar
st.sidebar.title("EcoRoute Assistant")
if st.sidebar.button("💬 Ask EcoRoute Assistant"):
    inventory_df = st.session_state.get("inventory_df")
    routes_df = st.session_state.get("routes_df")
    if inventory_df is None or routes_df is None:
        st.sidebar.error("Please upload both inventory and route data first.")
    else:
        # Add predicted_waste and carbon_score if not present
        if "predicted_waste" not in inventory_df.columns:
            inventory_df = inventory_df.copy()
            inventory_df["predicted_waste"] = 0
        if "carbon_score" not in routes_df.columns:
            routes_df = routes_df.copy()
            routes_df["carbon_score"] = 0
        with st.spinner("EcoRoute Assistant is thinking..."):
            advice = llm_agent.get_sustainability_advice(inventory_df, routes_df)
        st.sidebar.markdown("**EcoRoute Assistant says:**")
        st.sidebar.markdown(advice)

# Render the selected page
page = PAGES[selection]
page.render() 