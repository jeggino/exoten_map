import streamlit as st

import folium
from folium.plugins import Draw, Fullscreen, LocateControl
from streamlit_folium import st_folium

import pandas as pd

from streamlit_gsheets import GSheetsConnection

from constants import *



conn = st.connection("gsheets", type=GSheetsConnection)

def map(OUTPUT_width,OUTPUT_height):
    
    m = folium.Map(tiles=None)
  
    Draw(draw_options={'circle': False,'rectangle': False,'circlemarker': False, 'polyline': False, 'polygon': True},
        position="topright",).add_to(m)        
    Fullscreen(position="topright").add_to(m)
    LocateControl(auto_start=True,position="topright").add_to(m)

    folium.TileLayer(tiles='https://api.mapbox.com/styles/v1/jeggino/cm2vtvb2l000w01qz9wet0mv9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiamVnZ2lubyIsImEiOiJjbHdscmRkZHAxMTl1MmlyeTJpb3Z2eHdzIn0.N9TRN7xxTikk235dVs1YeQ',
                 attr='XXX Mapbox Attribution',overlay=False,show=True,name="Satellietkaart").add_to(m)
    folium.TileLayer(tiles="CartoDB Positron",overlay=False,show=False,name="Witte kaart").add_to(m)
    

    folium.LayerControl().add_to(m)
    
    output = st_folium(m, returned_objects=["all_drawings"],width=OUTPUT_width, height=OUTPUT_height)
    output["features"] = output.pop("all_drawings")
    
    return  output


def insert_json(key,waarnemer,datum,species,geometry_type,lat,lng,opmerking,coordinates,df_old):
    
    data = [{"key":key, "waarnemer":waarnemer,"datum":datum,"species":species, 
             "geometry_type":geometry_type,"lat":lat,"lng":lng,"opmerking":opmerking,"coordinates":coordinates}]
    df_new = pd.DataFrame(data)
    df_updated = pd.concat([df_old,df_new],ignore_index=True)
    
    return conn.update(worksheet="df_observations",data=df_updated)


@st.dialog(" ")
def input_data(output,df_old):
    waarnemer = st.session_state.login['name']    
    datum = st.date_input("Datum","today")       
    species = st.selectbox("Soort", SPECIES_LIST)
    opmerking = st.text_input("", placeholder="Vul hier een opmerking in ...")

    geometry_type = output["features"][0]["geometry"]["type"]
    
    st.divider()

    placeholder = st.empty()
    submitted = placeholder.button("**Gegevens opslaan**",use_container_width=True)
    if submitted:           
        coordinates = output["features"][0]["geometry"]["coordinates"] 
        
        if geometry_type in ["LineString",'Polygon']:

            lng = coordinates[0][0][0]
            lat = coordinates[0][0][1]
            key = str(lng)+str(lat)
        
        else: 
            
            lng = coordinates[0]
            lat = coordinates[1]
            coordinates = None
            
            key = str(lng)+str(lat)

        if len(output["features"]) > 1:
            st.error("U kunt niet meer dan één waarneming tegelijk uploaden!")
            st.stop()

        else:
            placeholder.success('Gegevens opgeslagen!', icon="✅",)
            insert_json(key,waarnemer,str(datum),species,geometry_type,lat,lng,opmerking,coordinates,df_old)
        
        st.switch_page("page/🧭_navigatie.py")
