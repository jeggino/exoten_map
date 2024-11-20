import streamlit as st
from streamlit_gsheets import GSheetsConnection



from constants import *
from functions.inputs import map,input_data
from css import *



#---LAYOUT---
st.markdown(collapsedControl,unsafe_allow_html=True,)
st.markdown(header_hidden,unsafe_allow_html=True)
st.markdown(reduce_header_height_style, unsafe_allow_html=True)


# --- APP ---  
# try:
st.logo(IMAGE,  link=None, icon_image=IMAGE)

waarnemer = st.session_state.login['name']
conn = st.connection("gsheets", type=GSheetsConnection)
df_old = conn.read(ttl=ttl_df_points,worksheet="df_observations")

output_map = map(OUTPUT_width,OUTPUT_height)

try:
    if len(output_map["features"]) >= 1:
        input_data(output_map,df_old)
        
    else:
        st.stop()      
        
except:
    st.stop()
    
# except:
#     st.switch_page("page/🧭_navigatie.py")
