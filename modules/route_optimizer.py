import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

def get_color(score):
    if score >= 80:
        return "green"
    elif score >= 60:
        return "yellow"
    else:
        return "red"

def calculate_carbon(distance, vehicle_type):
    if vehicle_type == "EV":
        return distance * 0.03
    else:
        return distance * 0.22

def render():
    st.title("Route Optimizer")
    if "routes_df" not in st.session_state:
        st.warning("Please upload routes data on the Data Upload page.")
        return
    routes_df = st.session_state["routes_df"].copy()
    sources = routes_df["source"].unique()
    destinations = routes_df["destination"].unique()
    source = st.selectbox("Select Source", sources)
    destination = st.selectbox("Select Destination", destinations)
    filtered = routes_df[(routes_df["source"] == source) & (routes_df["destination"] == destination)].copy()
    if filtered.empty:
        st.info("No routes found for this source-destination pair.")
        return
    filtered["carbon_kg"] = filtered.apply(lambda r: calculate_carbon(r["distance_km"], r["vehicle_type"]), axis=1)
    st.subheader("Route Comparison Table")
    st.dataframe(filtered[["route_id", "distance_km", "vehicle_type", "carbon_kg"]])
    best_route = filtered.sort_values("carbon_kg").iloc[0]
    st.success(f"Best Eco-Friendly Route: {best_route['route_id']} (Carbon: {best_route['carbon_kg']:.2f} kg)")
    # Optional: Map visualization (dummy coordinates)
    m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
    folium.Marker([37.1, -95.7], tooltip=f"Source: {source}").add_to(m)
    folium.Marker([37.2, -95.6], tooltip=f"Destination: {destination}").add_to(m)
    folium.PolyLine([[37.1, -95.7], [37.2, -95.6]], color="green").add_to(m)
    st_folium(m, width=700, height=400)
    st.subheader("Sustainability Scores by Route")
    styled_df = routes_df[["route_id", "source", "destination", "distance_km", "vehicle_type", "carbon_score", "predicted_waste", "sustainability_score"]].copy()
    def color_score(val):
        color = get_color(val)
        return f"background-color: {color}"
    st.dataframe(
        styled_df.style.applymap(color_score, subset=["sustainability_score"])
    )
    # Download button
    csv = routes_df.to_csv(index=False)
    st.download_button("Download Sustainability Report", csv, "sustainability_report.csv", "text/csv") 