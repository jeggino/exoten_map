import streamlit as st
from streamlit_gsheets import GSheetsConnection

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

import pandas as pd
import datetime
from datetime import datetime, timedelta, date
import ast

from functions.login import logOut
from functions.popup import popup_polygons,popup_points
from constants import *
from css import *


#---LAYOUT---
st.markdown(collapsedControl,unsafe_allow_html=True,)
st.markdown(header_hidden,unsafe_allow_html=True)
st.markdown(reduce_header_height_style, unsafe_allow_html=True)


#---DATASET---
conn = st.connection("gsheets", type=GSheetsConnection)
df_point = conn.read(ttl=ttl_df_points ,worksheet="df_observations")
df_point 

#---APP---
st.logo(IMAGE,  link=None, icon_image=IMAGE)

with st.sidebar:
    logOut()

try:
  st.sidebar.subheader("Filter op",divider=False)
  df_point["datum"] = pd.to_datetime(df_point["datum"]).dt.date
  d = st.sidebar.slider("Datum", min_value=df_point.datum.min(),max_value=df_point.datum.max(),
                          value=(df_point.datum.min(), df_point.datum.max()),format="DD-MM-YYYY")
    
  df_point_filtered = df_point[(df_point['datum']>=d[0]) & (df_point['datum']<=d[1])]
  species_filter_option = df_point_filtered["species"].unique()
  species_filter = st.sidebar.multiselect("Sorten",species_filter_option,species_filter_option)
  df_point_filtered = df_point_filtered[df_point_filtered['species'].isin(species_filter)]
  species_colors_dict=dict(zip(species_filter_option,COLORS[:len(species_filter_option)]))
  df_point_filtered['color'] = df_point_filtered['species'].map(species_colors_dict)
  
except:
    pass

st.sidebar.divider()


 
map = folium.Map(tiles=None)
LocateControl(auto_start=True,position="topright").add_to(map)
Fullscreen(position="topright").add_to(map)

points = folium.FeatureGroup(name='Punten')
areas = folium.FeatureGroup(name='Gebieden')

folium.TileLayer('OpenStreetMap',overlay=False,show=True,name="Stratenkaart").add_to(map)
folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False,name="Witte kaart").add_to(map)
folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/jeggino/cm2vtvb2l000w01qz9wet0mv9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamVnZ2lubyIsImEiOiJjbHdscmRkZHAxMTl1MmlyeTJpb3Z2eHdzIn0.N9TRN7xxTikk235dVs1YeQ',
                 attr='XXX Mapbox Attribution',overlay=False,show=False,name="Satellietkaart").add_to(map)

try:
  for i in range(len(df_point_filtered)):
  
      if df_point_filtered.iloc[i]['geometry_type'] == "Point":
              
  
          html = popup_html(i,df_point)
          popup = folium.Popup(folium.Html(html, script=True), max_width=300)
  
          folium.Marker([df_2.iloc[i]['lat'], df_2.iloc[i]['lng']],
                        popup=popup,
                        icon=folium.Icon(icon='plant',
                                         prefix='fa',
                                         icon_color='black',
                                         color=df_point_filtered.iloc[i]['color'],)
                       ).add_to(points)
  
      elif df_point_filtered.iloc[i]['geometry_type'] == "Polygon":
          html = popup_polygons(i,df_point)
          popup = folium.Popup(folium.Html(html, script=True), max_width=300)
          location = df_point_filtered.iloc[i]['coordinates']
          location = ast.literal_eval(location)
          location = [i[::-1] for i in location[0]]
              
          folium.Polygon(location,
                         fill_color=df_point_filtered.iloc[i]['color'],
                         weight=0,
                         fill_opacity=0.5,
                         popup=popup
                        ).add_to(areas)

except:
  pass

folium.LayerControl().add_to(map)

output = st_folium(map,returned_objects=["last_active_drawing"],width=OUTPUT_width, height=OUTPUT_height,
                     feature_group_to_add=[points,areas])


# except:
#     st.image("https://media.istockphoto.com/photos/open-empty-cardboard-box-on-a-white-background-picture-id172167710?k=6&m=172167710&s=612x612&w=0&h=Z4fueCweh9q-X_VBRAPCYSalyaAnXG3ioErb8oJSVek=")
#     st.stop()
