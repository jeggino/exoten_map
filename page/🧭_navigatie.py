import streamlit as st
from streamlit_gsheets import GSheetsConnection

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium
from branca.element import Template, MacroElement, IFrame

import pandas as pd
import datetime
from datetime import datetime, timedelta, date
import ast

from functions.legend import legend
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
df_point_filtered =  df_point.copy()

#---APP---
st.logo(IMAGE,  link=LINK, icon_image=IMAGE)

if len(df_point_filtered)>0:
  st.sidebar.subheader("Filter op",divider=False)
  
  df_point_filtered["datum"] = pd.to_datetime(df_point_filtered["datum"]).dt.date
  
  try:
    d = st.sidebar.slider("Datum", min_value=df_point_filtered.datum.min(),max_value=df_point_filtered.datum.max(),
                            value=(df_point_filtered.datum.min(), df_point_filtered.datum.max()),format="DD-MM-YYYY")
    df_point_filtered = df_point_filtered[(df_point_filtered['datum']>=d[0]) & (df_point_filtered['datum']<=d[1])]
    
  except:
    pass
  
  species_filter_option = df_point_filtered["species"].unique()
  species_filter = st.sidebar.multiselect("Sorten",species_filter_option,species_filter_option)
  df_point_filtered = df_point_filtered[df_point_filtered['species'].isin(species_filter)]
  
  species_colors_dict=dict(zip(species_filter_option,COLORS[:len(species_filter_option)]))
  df_point_filtered['color'] = df_point_filtered['species'].map(species_colors_dict)

st.sidebar.divider()


 
map = folium.Map(tiles=None)
LocateControl(auto_start=True,position="topright").add_to(map)
Fullscreen(position="topright").add_to(map)

points = folium.FeatureGroup(name='Punten').add_to(map)
areas = folium.FeatureGroup(name='Gebieden').add_to(map)

folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/jeggino/cm2vtvb2l000w01qz9wet0mv9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamVnZ2lubyIsImEiOiJjbHdscmRkZHAxMTl1MmlyeTJpb3Z2eHdzIn0.N9TRN7xxTikk235dVs1YeQ',
                 attr='XXX Mapbox Attribution',overlay=False,show=True,name="Satellietkaart").add_to(map)
folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False,name="Witte kaart").add_to(map)


try:
  for i in range(len(df_point_filtered)):
  
      if df_point_filtered.iloc[i]['geometry_type'] == "Point":
        html = popup_points(i,df_point_filtered)
        popup = folium.Popup(folium.Html(html, script=True), max_width=300)
        
        folium.Marker([df_point_filtered.iloc[i]['lat'], df_point_filtered.iloc[i]['lng']],
          popup=popup,
          icon=folium.Icon(icon="fa-brands fa-pagelines",
          prefix='fa',
          icon_color='black',
          color=df_point_filtered.iloc[i]['color'],)
          ).add_to(points)
  
      elif df_point_filtered.iloc[i]['geometry_type'] == "Polygon":
        html = popup_polygons(i,df_point_filtered)
        popup = folium.Popup(folium.Html(html, script=True), max_width=300)
        location = df_point_filtered.iloc[i]['coordinates']
        location = ast.literal_eval(location)
        location = [i[::-1] for i in location[0]]
              
        folium.Polygon(location,
                       color="black",
                       fill_color=df_point_filtered.iloc[i]['color'],
                       weight=2,
                       fill_opacity=0.5,
                       popup=popup
                      ).add_to(areas)
  
  
  
  
  
  legend_template = legend(species_colors_dict,False)
  macro = MacroElement()
  macro._template = Template(legend_template)
  map.add_child(macro)
  

except:
  pass

folium.LayerControl().add_to(map)

output = st_folium(map,returned_objects=["last_active_drawing"],width=OUTPUT_width, height=OUTPUT_height,
                     feature_group_to_add=[points,areas])

if st.session_state.login['option_user'] == 'Gebruiker':
  
  try:
    
      try:
          id = str(output["last_active_drawing"]['geometry']['coordinates'][0])+str(output["last_active_drawing"]['geometry']['coordinates'][1])
          name = f"{id}"
      except:
          id = str(output["last_active_drawing"]['geometry']['coordinates'][0][0][0])+str(output["last_active_drawing"]['geometry']['coordinates'][0][0][1])
          name = f"{id}"
  
      with st.sidebar:
          # if st.button("Waarneming bijwerken",use_container_width=True):
          #     update_item()
          with st.form("entry_form", clear_on_submit=True,border=False):
              submitted = st.form_submit_button(":red[**Verwijder waarneming**]",use_container_width=True)
              if submitted:
                  df = conn.read(ttl=0,worksheet="df_observations")
                  df_filter = df[df["key"]==id]
                  df_drop = df[~df.apply(tuple, axis=1).isin(df_filter.apply(tuple, axis=1))]
                  conn.update(worksheet='df_observations',data=df_drop)
                  st.success('Waarneming verwijderd', icon="✅") 
                  st.page_link("page/🧭_navigatie.py", label="Vernieuwen", icon="🔄",use_container_width=True)

  except:
      pass
