import streamlit as st
from streamlit_gsheets import GSheetsConnection

from constants import *


conn = st.connection("gsheets", type=GSheetsConnection)
df_users = conn.read(ttl=ttl_df_users ,worksheet="df_users")


def logIn(df_users):
    option_user = st.selectbox("Selecteer of u een gast of een gebruikersaccount bent. Bedankt.",("Gast", "Gebruiker"),index = None)
    
    if option_user == None:
        st.stop()

    elif option_user == "Gebruiker": 
        name = st.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
        password = st.text_input("Vul uw wachtwoord in, alstublieft")
        
        try:
            if name == None:
                st.stop()
            
            index = df_users[df_users['username']==name].index[0]
            true_password = df_users.loc[index,"password"]
    
        except:
            st.warning("De gebruikersnaam is niet correct.")
            st.stop()
            
    elif option_user == "Gast":
        name = None
        password = None
                             
    if st.button("logIn",use_container_width=True):
        if password == true_password:
            st.session_state.login = {"name": name, "password": password}
            st.rerun()

        else:
            st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")

