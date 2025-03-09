import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import os
import folium

st.title("Business Catalogue")

if os.path.exists("business_data.csv"):
    existing_data = pd.read_csv("business_data.csv")
else:
    existing_data = pd.DataFrame(columns=["poi_name", "phone", "latitude", "longitude"])


with st.form("Input your business data"):
    data = {}
    data["poi_name"] = st.text_input("Business name")
    data["phone"] = st.text_input("Phone number")
    data["latitude"] = st.number_input("Latitude", format="%.6f")
    data["longitude"] = st.number_input("Longitude", format="%.6f")

    submitted = st.form_submit_button("Submit")

st.subheader("Maps")

# Set dynamic map center
if not existing_data.empty:
    min_lat, max_lat = existing_data["latitude"].min(), existing_data["latitude"].max()
    min_lon, max_lon = (
        existing_data["longitude"].min(),
        existing_data["longitude"].max(),
    )

    # Set center as the mean position
    avg_lat = existing_data["latitude"].mean()
    avg_lon = existing_data["longitude"].mean()

    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
else:
    avg_lat, avg_lon = -6.2, 106.8  # Default location (Jakarta)
    bounds = None

# Initialize map centered at average location
m = folium.Map(location=[avg_lat, avg_lon], zoom_start=12)

# Add markers
fg = folium.FeatureGroup(name="Business POI")
for _, business in existing_data.iterrows():
    fg.add_child(
        folium.Marker(
            location=[business.latitude, business.longitude],
            popup=business.poi_name,
            tooltip=business.poi_name,
            icon=folium.Icon(color="green"),
        )
    )

m.add_child(fg)

# Adjust zoom dynamically based on bounds
if bounds:
    m.fit_bounds(bounds)

st_data = st_folium(m, width=1200, height=500)

if submitted:
    if not data["poi_name"] or not data["phone"]:
        st.warning("Business name and phone number cannot be empty!")
    elif data["latitude"] == 0.0 or data["longitude"] == 0.0:
        st.warning("Latitude and Longitude cannot be 0.")
    else:
        df_data = pd.DataFrame([data])
        df_data.to_csv(
            "business_data.csv",
            mode="a",
            header=not os.path.exists("business_data.csv"),
        )
        st.success("Data saved successfully!")
        st.rerun()
