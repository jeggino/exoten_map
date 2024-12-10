import streamlit as st

# Initialize connection.
conn = st.connection('mysql', type='sql')
st.write('OK')
# # Perform query.
df = conn.query('SELECT * from mytable;', ttl=600)

# import streamlit as st
# from streamlit_gsheets import GSheetsConnection

# from constants import *
# from css import *
# from functions.login import logIn



# #---LAYOUT---
# st.markdown(collapsedControl,unsafe_allow_html=True,)
# st.markdown(header_hidden,unsafe_allow_html=True)
# st.markdown(reduce_header_height_style, unsafe_allow_html=True)


# #---DATASET---
# conn = st.connection("gsheets", type=GSheetsConnection)
# df_users = conn.read(ttl=ttl_df_users,worksheet="df_users")


# #---APP---
# page_1 = st.Page("page/🧭_navigatie.py", title="Navigatie",icon="🧭" )
# page_2 = st.Page("page/✍️_Voeg_een_waarneming_in.py", title="Voeg een waarneming in",icon="✍️" )
# # page_3 = st.Page("page/↩️_Update_een_locatie.py", title="Update een locatie",icon="↩️" )
# # page_4 = st.Page("page/📊_ Statistik.py", title="Statistik",icon="📊" )

# #---APP---
# st.logo(IMAGE,  link=LINK, icon_image=IMAGE)

    
# if "login" not in st.session_state:
#     logIn(df_users)
#     st.stop()

# if st.session_state.login['option_user'] == 'Gebruiker':
#     pg = st.navigation([page_1,page_2])
#     pg.run()

# elif st.session_state.login['option_user'] == 'Gast':
#     pg = st.navigation([page_1])
#     pg.run()
