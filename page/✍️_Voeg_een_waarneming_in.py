import streamlit as st
from streamlit_gsheets import GSheetsConnection



from constants import *
from functions.inputs import map,input_data



st.markdown("""
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137, .viewerBadge_text__1JaDK{ display: none; } #MainMenu{ visibility: hidden; } footer { visibility: hidden; } header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True)



reduce_header_height_style = """
<style>
    div.block-container {padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; margin-top: 1rem; margin-bottom: 0rem;}
</style>
""" 

st.markdown(reduce_header_height_style, unsafe_allow_html=True)


# --- APP ---  
try:
    st.logo(IMAGE,  link=None, icon_image=IMAGE_2)
    
    waarnemer = st.session_state.login['name']
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_old = conn.read(ttl=ttl_df_points,worksheet="df_observations")
    
    output_map = map()
    
    try:
        if len(output_map["features"]) >= 1:
            input_data(output_map,df_old)
            
        else:
            st.stop()      
            
    except:
        st.stop()
    
except:
    st.switch_page("page/🧭_navigatie.py")
