import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

# =========================
# HEADER
# =========================

def show_header(text_title: str):
    col1, col2 = st.columns([1, 6])

    with col1:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/3/32/Universidad_Panamericana_Logo_Dorado.jpg",
            width=120
        )

    with col2:
        st.title(text_title)
        st.caption("📘 Developed for: Business Intelligence")
        st.caption("Universidad Panamericana")


header_container = st.container()
main_container = st.container()

with header_container:
    show_header("Dashboard Ecobici CDMX")

# =========================
# DATA EXTRACTION
# =========================

url = "https://gbfs.mex.lyftbikes.com/gbfs/gbfs.json"

pagina = requests.get(url).json()
ligas = pagina['data']['es']['feeds']

liga1, liga2 = [liga for liga in ligas if 'station' in liga['name']]

df1 = pd.DataFrame(
    requests.get(liga1['url']).json()['data']['stations']
).iloc[:, :5]

df2 = pd.DataFrame(
    requests.get(liga2['url']).json()['data']['stations']
)[['station_id', 'name', 'lat', 'lon', 'capacity']]

df = pd.concat([df1, df2], axis=1)

# =========================
# MAIN CONTENT
# =========================

with main_container:

    st.markdown("## 🚲 Ecobici Stations in Mexico City")

    st.dataframe(df.head())

    st.markdown("### Interactive Map")

    centroide_lat = df['lat'].mean()
    centroide_lon = df['lon'].mean()

    mapa = folium.Map(
        location=[centroide_lat, centroide_lon],
        zoom_start=12
    )

    for i in range(len(df)):
        folium.Marker(
            location=[df['lat'][i], df['lon'][i]],
            popup=df['name'][i]
        ).add_to(mapa)

    st_folium(mapa, width=700, height=500)
