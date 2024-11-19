import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import geopandas as gpd
import random

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium
import datetime
from datetime import datetime, timedelta, date
import random

import ast

from credentials import *



#---DATASET---
ttl = '30m'
ttl_references = '30m'
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl,worksheet="df_observations")
df_references = conn.read(ttl=ttl_references,worksheet="df_users")


st.markdown(
    """
    <style>
    [data-testid="collapsedControl"] svg {
        height: 0rem;
        width: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)



reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 0rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)


# --- DIMENSIONS ---
OUTPUT_width = '95%'
OUTPUT_height = 550


#---APP---
IMAGE = "image/logo.png"
IMAGE_2 ="image/menu.jpg"
st.logo(IMAGE_2,  link=None, icon_image=IMAGE_2)


df_point["datum"] = pd.to_datetime(df_point["datum"]).dt.date

try:
  st.sidebar.subheader("Filter op",divider=False)
  d = st.sidebar.slider("Datum", min_value=df_point.datum.min(),max_value=df_point.datum.max(),
                          value=(df_point.datum.min(), df_point.datum.max()),format="DD-MM-YYYY")
    
  df_point = df_point[(df_point['datum']>=d[0]) & (df_point['datum']<=d[1])]
except:
    pass

  species_filter_option = df_2["sp"].unique()
  species_filter = st.sidebar.multiselect("Sorten",species_filter_option,species_filter_option)
  df_point = df_point[df_point['sp'].isin(species_filter)]

st.sidebar.divider()

try:
    df_2["icon_data"] = df_2.apply(lambda x: None if x["geometry_type"] in ["LineString","Polygon"] 
                                   else (icon_dictionary[x["soortgroup"]][x["sp"]][x["functie"]] if x["soortgroup"] in ['Vogels','Vleermuizen',"Vogels-Overig"] 
                                         else icon_dictionary[x["soortgroup"]][x["functie"]]), 
                                   axis=1)
    
    df_2 = df_2.reset_index(drop=True)
except:
    pass
 
map = folium.Map(tiles=None)

if st.session_state.project['auto_start']==True:
    auto_start = False
else:
    auto_start = True
LocateControl(auto_start=True,position="topright").add_to(map)
Fullscreen(position="topright").add_to(map)

functie_dictionary = {}

try:
    functie_len = df_2['functie'].unique()
    
    for functie in functie_len:
        functie_dictionary[functie] = folium.FeatureGroup(name=functie)    
    
    for feature_group in functie_dictionary.keys():
        map.add_child(functie_dictionary[feature_group])
except:
    pass

functie_dictionary['geometry'] = folium.FeatureGroup(name='Geometries')

folium.TileLayer('OpenStreetMap',overlay=False,show=True,name="Stratenkaart").add_to(map)
folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False,name="Witte kaart").add_to(map)
folium.TileLayer(tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',attr='Google_map',overlay=False,show=False,name="Satellietkaart").add_to(map)

try:
    folium.GeoJson(
        st.session_state.project['gdf'],
        name=f"*Gebied: {st.session_state.project['area']}",
        style_function=lambda feature: {
            "color": "black",
            "weight": 1,
        },
    ).add_to(map)
except:
    pass
    
for i in range(len(df_2)):

    if df_2.iloc[i]['geometry_type'] == "Point":

        if (df_2.iloc[i]['sp']=="Huismus"):
            ICON_SIZE_2 = ICON_SIZE_huismus


        elif (df_2.iloc[i]['sp'] in ['Laatvlieger','Rosse vleermuis','Meervleermuis','Watervleermuis']):
            ICON_SIZE_2 = ICON_SIZE_BAT_EXTRA

        elif (df_2.iloc[i]['sp'] in ['Ruige dwergvleermuis']):
            ICON_SIZE_2 = ICON_SIZE_RUIGE

        elif (df_2.iloc[i]['sp']=="...Andere(n)") & (df_2.iloc[i]['soortgroup'] == 'Vogels-Overig'):
            ICON_SIZE_2 = ICON_SIZE_BIRD

        elif (df_2.iloc[i]['sp'] == '...Andere(n)') & (df_2.iloc[i]['soortgroup'] == 'Vleermuizen'):
            ICON_SIZE_2 = ICON_SIZE

        elif (df_2.iloc[i]['sp'] == 'Huiszwaluw'):
            ICON_SIZE_2 = ICON_SIZE_Huiszwaluw

        else:             
            ICON_SIZE_2 = ICON_SIZE
            

        html = popup_html(i)
        popup = folium.Popup(folium.Html(html, script=True), max_width=300)
        fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]

        folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                      popup=popup,
                      icon=folium.features.CustomIcon(df_2.iloc[i]["icon_data"], icon_size=ICON_SIZE_2)
                     ).add_to(fouctie_loop)

    elif df_2.iloc[i]['geometry_type'] == "Polygon":
        html = popup_polygons(i)
        popup = folium.Popup(folium.Html(html, script=True), max_width=300)
        fouctie_loop = functie_dictionary[df_2.iloc[i]['functie']]
        location = df_2.iloc[i]['coordinates']
        location = ast.literal_eval(location)
        location = [i[::-1] for i in location[0]]
                    
        if df_2.iloc[i]['functie']=="Baltsterritorium":
            fill_color="red"

        else:
            fill_color="green"
            
        folium.Polygon(location,fill_color=fill_color,weight=0,fill_opacity=0.5,
                      popup=popup
                      ).add_to(fouctie_loop)

folium.LayerControl().add_to(map)

output = st_folium(map,returned_objects=["last_active_drawing"],width=OUTPUT_width, height=OUTPUT_height,
                     feature_group_to_add=list(functie_dictionary.values()))


# except:
#     st.image("https://media.istockphoto.com/photos/open-empty-cardboard-box-on-a-white-background-picture-id172167710?k=6&m=172167710&s=612x612&w=0&h=Z4fueCweh9q-X_VBRAPCYSalyaAnXG3ioErb8oJSVek=")
#     st.stop()
