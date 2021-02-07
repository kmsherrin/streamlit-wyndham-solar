import streamlit as st
import pandas as pd
import numpy as np
import json
import pydeck as pdk

single_df = pd.read_csv('data/single_entry_each_site.csv')

#menu = st.sidebar.title("Menu")

st.title('Wyndham Solar Project')

"""
### Table of the different sites
"""
single_df[['system_name', 'date_installed', 'lat', 'lon']]


option = st.selectbox('Select a site:', single_df['system_name'])

st.write('Highlighting location: ', option)

map_data = single_df[['lat', 'lon', 'system_name']]

selected_map_data = map_data.loc[map_data['system_name'] == option]
reduced_map_data = map_data.loc[map_data['system_name'] != option]

r = pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=-37.86,
         longitude=144.74,
         zoom=10,
         pitch=0,
     ),
     layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=reduced_map_data,
             pickable=True,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=selected_map_data,
             pickable=True,
             get_position='[lon, lat]',
             get_color='[52, 235, 52, 160]',
             get_radius=300,
         ),
     ],
        tooltip={"text": "{system_name}"}
     )

st.pydeck_chart(r)

#system_name_subset = 