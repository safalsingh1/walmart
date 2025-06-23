import streamlit as st
import pandas as pd

def render():
    st.title("Data Upload")
    st.write("Upload your inventory and route data as CSV files.")

    inventory_file = st.file_uploader("Upload inventory.csv", type=["csv"], key="inventory")
    routes_file = st.file_uploader("Upload routes.csv", type=["csv"], key="routes")

    if inventory_file:
        inventory_df = pd.read_csv(inventory_file)
        st.session_state["inventory_df"] = inventory_df
        st.subheader("Inventory Data Preview")
        st.dataframe(inventory_df.head())
    else:
        st.info("Please upload inventory.csv")

    if routes_file:
        routes_df = pd.read_csv(routes_file)
        st.session_state["routes_df"] = routes_df
        st.subheader("Routes Data Preview")
        st.dataframe(routes_df.head())
    else:
        st.info("Please upload routes.csv") 