import streamlit as st
from streamlit_gsheets import GSheetsConnection

from constants import *
from functions.login import logIn


conn = st.connection("gsheets", type=GSheetsConnection)
df_users = conn.read(ttl=ttl_df_users,worksheet="df_users")

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



#---APP---
page_1 = st.Page("page/🧭_navigatie.py", title="Navigatie",icon="🧭" )
page_2 = st.Page("page/✍️_Voeg_een_waarneming_in.py", title="Voeg een waarneming in",icon="✍️" )
# page_3 = st.Page("page/↩️_Update_een_locatie.py", title="Update een locatie",icon="↩️" )
# page_4 = st.Page("page/📊_ Statistik.py", title="Statistik",icon="📊" )

#---APP---
IMAGE = "image/logo.png"
st.logo(IMAGE_2,  link=None, icon_image=IMAGE_2)

st.image("https://www.elskenecologie.nl/wp-content/uploads/2023/08/terschelling.jpg")
option_user = st.selectbox("Selecteer of u een gast of een gebruikersaccount bent. Bedankt.",("Gast", "Gebruiker"),index = None)

if option_user == None:
    st.stop()

elif option_user == "Gast":
    pg = st.navigation([page_1])

elif option_user == "Gebruiker":
    
    if "login" not in st.session_state:
        logIn(df_users)
        st.stop()

    else:
        pg = st.navigation([page_1,page_2])
        pg.run()
