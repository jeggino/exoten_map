import streamlit as st
from streamlit_gsheets import GSheetsConnection

from constants import *
from css import *
from functions.login import logIn





#---LAYOUT---
st.markdown(collapsedControl,unsafe_allow_html=True,)
st.markdown(header_hidden,unsafe_allow_html=True)
st.markdown(reduce_header_height_style, unsafe_allow_html=True)


#---DATASET---
conn = st.connection("gsheets", type=GSheetsConnection)
df_users = conn.read(ttl=ttl_df_users,worksheet="df_users")


#---APP---
page_1 = st.Page("page/🧭_navigatie.py", title="Navigatie",icon="🧭" )
page_2 = st.Page("page/✍️_Voeg_een_waarneming_in.py", title="Voeg een waarneming in",icon="✍️" )
# page_3 = st.Page("page/↩️_Update_een_locatie.py", title="Update een locatie",icon="↩️" )
# page_4 = st.Page("page/📊_ Statistik.py", title="Statistik",icon="📊" )

#---APP---
st.logo(IMAGE,  link=None, icon_image=IMAGE)

col_1,col_2 = st.columns([2,1])

placeholder = st.empty()
with col_1:
    placeholder.image("https://www.elskenecologie.nl/wp-content/uploads/2023/08/terschelling.jpg")
with col_2:    
    option_user = placeholder.selectbox("Selecteer of u een gast of een gebruikersaccount bent. Bedankt.",("Gast", "Gebruiker"),index = None)

if option_user == None:
    st.stop()

elif option_user == "Gast":
    placeholder.empty()
    pg = st.navigation([page_1])
    pg.run()

elif option_user == "Gebruiker":
    
    if "login" not in st.session_state:
        with col_2:
            logIn(df_users)
            st.stop()

    else:
        pg = st.navigation([page_1,page_2])
        pg.run()
        placeholder.empty()
