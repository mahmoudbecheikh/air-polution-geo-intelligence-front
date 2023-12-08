from io import StringIO
import streamlit as st
import pandas as pd
import plotly.express as px
from random import choice
import pydeck as pdk
import pandas as pd
import streamlit.components.v1 as components
import requests
from utils import color_aqi

def get_api_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        object_data = response.json()
        return pd.DataFrame(object_data['data'])
    else:
        return None

countries = [country[0] for country in get_api_data('http://20.67.251.38/countries').map(str.capitalize).values.tolist()]
countries.insert(0, "Touts")

def get_quote():
    with open(r"quotes.txt", mode="r",encoding="utf8") as file:
        quotes = file.readlines()
    return choice(quotes)

with st.sidebar:
    st.title("🌱Il n’y a pas de planète B ")
    st.subheader("«Greta thunberg»")


    regionSelected = st.selectbox("Régions", countries)
    data_type = st.selectbox("Type de donnée", ['Valeur globale de l’indice de qualité de l’air', 'Valeur de l’indice de qualité de l’air de l’ozone'])
    st.header("_**Citations du jour**_")
    st.caption(get_quote())


if data_type == 'Valeur globale de l’indice de qualité de l’air':
    data = get_api_data("http://20.67.251.38/?type=carbon")
    data["exits_radius"] = data["aqi_value"].map(lambda x : x * 100)
    data["color"] = data["aqi_category"].map(color_aqi)
else:
    data = get_api_data("http://20.67.251.38/?type=ozone")
    data["exits_radius"] = data["ozone_aqi_value"].map(lambda x : x * 100)
    data["color"] = data["ozone_aqi_category"].map(color_aqi)



layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=3,
    radius_min_pixels=3,
    radius_max_pixels=30,
    line_width_min_pixels=1,
    get_position="coordinates",
    get_radius="exits_radius",
    get_fill_color="color",
    get_line_color=[0, 0, 0],
)

if regionSelected == 'Touts':
    view_state = pdk.ViewState(latitude=48.85667, longitude= 2.35222, zoom=4,aring=0, pitch=0)
else:
    country_df = get_api_data(f"http://20.67.251.38?country={regionSelected.lower()}")
    coordinates = country_df.iloc[0]['coordinates']
    view_state = pdk.ViewState(latitude=coordinates[1], longitude=coordinates[0], zoom=4,aring=0, pitch=0)

tooltip = {"html": "<b>{name_fr}</b>", "style": {"backgroundColor": "steelblue", "color": "white"}}
r = pdk.Deck(layers=[layer],map_style="road", initial_view_state=view_state, tooltip={"text": "{country}\n{city}"})

st.title(f"🌱Géo carte interactive de {data_type} ")

st.pydeck_chart(r)

components.html("""
<style>
    .legend-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        background-color: #f8f8f8;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        margin-right: 20px;
        width : 250px ;
        heigth : 200px
                
    }

    .legend-item {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
    }

    .legend-color {
        width: 20px;
        height: 20px;
        margin-right: 8px;
        border-radius: 50%;
    }

    .legend-label {
        font-size: 14px;
        font-weight: bold;
    }

    .legend-source {
        font-size: 12px;
        color: #888;
    }
</style>
<div class='legend-container'>
    <div class='legend-item'>
        <div class='legend-color' style='background:#008000;'></div>
        <div class='legend-label'>Good</div>
    </div>
    <div class='legend-item'>
        <div class='legend-color' style='background:#FFFD37;'></div>
        <div class='legend-label'>Moderate</div>
    </div>
    <div class='legend-item'>
        <div class='legend-color' style='background:#ff8c00;'></div>
        <div class='legend-label'>Unhealthy</div>
    </div>
    <div class='legend-item'>
        <div class='legend-color' style='background:#ff0000;'></div>
        <div class='legend-label'>Dangerous</div>
    </div>
</div>
   """
)