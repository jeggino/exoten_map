import streamlit as st
from streamlit_gsheets import GSheetsConnection

from constants import *


conn = st.connection("gsheets", type=GSheetsConnection)
df_users = conn.read(ttl=ttl_df_users ,worksheet="df_users")


def logIn(df_users):
    col_1,col_2 = st.columns([3,2])
    col_1.image("https://www.elskenecologie.nl/wp-content/uploads/2023/08/terschelling.jpg")
    
    option_user = col_2.selectbox("Selecteer of u een gast of een gebruikersaccount bent. Bedankt.",("Gast", "Gebruiker"),index = None)
    
    if option_user == None:
        st.stop()

    elif option_user == "Gebruiker": 
        name = col_2.text_input("Vul uw gebruikersnaam in, alstublieft",value=None)  
        password = col_2.text_input("Vul uw wachtwoord in, alstublieft")
        
        try:
            if name == None:
                st.stop()
            
            index = df_users[df_users['username']==name].index[0]
            true_password = df_users.loc[index,"password"]
    
        except:
            col_2.warning("De gebruikersnaam is niet correct.")
            st.stop()
            
    elif option_user == "Gast":
        name = None
        password = None
                             
    if st.button("logIn",use_container_width=True):
        if option_user == "Gebruiker": 
            if password == true_password:
                st.session_state.login = {"name": name, "password": password, "option_user":option_user}
                st.rerun()
    
            else:
                st.markdown(f"Sorry {name.split()[0]}, het wachtwoord is niet correct.")

        elif option_user == "Gast":
            st.session_state.login = {"name": name, "password": password, "option_user":option_user}
            
        

