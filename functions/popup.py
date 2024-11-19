import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import datetime
from datetime import datetime, timedelta, date

import folium
from folium.plugins import Draw, Fullscreen, LocateControl, GroupedLayerControl
from streamlit_folium import st_folium

from credentials import *
import ast

def popup_polygons(row):
    
    i = row

    project=df_2['project'].iloc[i]
    gebied=df_2['gebied'].iloc[i]
    datum=df_2['datum'].iloc[i] 
    time=df_2['time'].iloc[i]
    sp = df_2['sp'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    aantal=df_2['aantal'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Project</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(project) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Gebied</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(gebied) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Tijd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(time) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soort</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sp) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(int(aantal)) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html


def popup_points(row):
    
    i = row

    project=df_2['project'].iloc[i]
    gebied=df_2['gebied'].iloc[i]
    datum=df_2['datum'].iloc[i] 
    time=df_2['time'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    sp = df_2['sp'].iloc[i] 
    functie=df_2['functie'].iloc[i]
    gedrag=df_2['gedrag'].iloc[i]
    verblijf=df_2['verblijf'].iloc[i]
    opmerking=df_2['opmerking'].iloc[i]
    aantal=df_2['aantal'].iloc[i]
    waarnemer=df_2['waarnemer'].iloc[i] 
       

    left_col_color = "#19a7bd"
    right_col_color = "#f2f0d3"
    
    html = """<!DOCTYPE html>
    <html>
    <table style="height: 126px; width: 300;">
    <tbody>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Project</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(project) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Gebied</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(gebied) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Datum</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(datum) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Tijd</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(time) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Soort</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(sp) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Functie</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(functie) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Gedrag</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(gedrag) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Verblijf</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(verblijf) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Opmerking</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(opmerking) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Aantal</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(int(aantal)) + """
    </tr>
    <tr>
    <td style="background-color: """+ left_col_color +""";"><span style="color: #ffffff;">Waarnemer</span></td>
    <td style="width: 150px;background-color: """+ right_col_color +""";">{}</td>""".format(waarnemer) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
    return html
