import streamlit as st
import pandas as pd
import numpy as np
import json
import pydeck as pdk
import altair as alt
import streamlit.components.v1 as components

st.set_page_config(page_title='Wyndham Solar Overview Viz')

def add_more_data(main_curr_option: str, sites_to_add: list):
    # Get clean version of inital data
    # Format the site name so that it can be used to grab the data from the Github URL
    selected_site_formatted = main_curr_option.replace(" ", "").lower()
    # Read in the selected site data from the github repo URL
    site_df = pd.read_csv(f'https://raw.githubusercontent.com/kmsherrin/streamlit-wyndham-solar/master/data/solar_farm_subset_{selected_site_formatted}.csv')
    site_df['date_stamp'] = pd.to_datetime(site_df['date_stamp'])

    # Now append the additional data necessary
    for site in sites_to_add:
        site_formatted = site.replace(" ", "").lower()
        add_site_df = pd.read_csv(f'https://raw.githubusercontent.com/kmsherrin/streamlit-wyndham-solar/master/data/solar_farm_subset_{site_formatted}.csv')
        add_site_df['date_stamp'] = pd.to_datetime(add_site_df['date_stamp'])

        site_df = site_df.append(add_site_df)

    return site_df

# Read in the data containing a location for every site
single_df = pd.read_csv('data/single_entry_each_site.csv')
#single_df = single_df.sort_values(by=['system_name'])

# Create some UI
st.title('Wyndham Solar Project')

"""
### Different Sites Overview
"""
# Display a table with the system names and their install dates
single_df[['system_name', 'date_installed', 'lat', 'lon']]

# Allow the user to select a site and have it highlighted on the map
option = st.selectbox('Select a site:', single_df['system_name'], index=0)

st.write('Highlighting location: ', option)

# There is the selected map data and reduced map data (one is the rest of the unselected list, the other is the selected site)
map_data = single_df[['lat', 'lon', 'system_name']]
selected_map_data = map_data.loc[map_data['system_name'] == option]
reduced_map_data = map_data.loc[map_data['system_name'] != option]

# Plot this on a pydeck map
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

# Format the site name so that it can be used to grab the data from the Github URL
selected_site_formatted = option.replace(" ", "").lower()
# Read in the selected site data from the github repo URL
site_df = pd.read_csv(f'https://raw.githubusercontent.com/kmsherrin/streamlit-wyndham-solar/master/data/solar_farm_subset_{selected_site_formatted}.csv')
site_df['date_stamp'] = pd.to_datetime(site_df['date_stamp'])


f"""
### Historical data for this site:

[view on github](https://github.com/kmsherrin/streamlit-wyndham-solar/blob/master/data/solar_farm_subset_{selected_site_formatted}.csv)

"""

# Display the charts
"""

## Historical Data Charts

"""

st.text(f'Currently showing data for the selected site: {option}')


overlay_sites = st.checkbox('Overlay additional sites?')

sites_to_add = []
if overlay_sites:
    sites_to_add = st.multiselect('Add site historical data', sorted(single_df.loc[single_df['system_name'] != option]['system_name']))
    site_df = add_more_data(option, sites_to_add)


"""
### Performance
"""
c = alt.Chart(site_df).mark_circle(size=60, color="#668dd1").encode(
    x='date_stamp',
    y='performance',
    color='system_name',
    tooltip=['system_name', 'date_stamp', 'performance', 'energy_prod(KWh)', 'C02 (Kg)']
).interactive()
st.altair_chart(c, use_container_width=True)

"""
### Energy Produced (KWh)
"""
c = alt.Chart(site_df).mark_circle(size=60, color="#66d196").encode(
    x='date_stamp',
    y='energy_prod(KWh)',
    color='system_name',
    tooltip=['system_name', 'date_stamp', 'energy_prod(KWh)']
).interactive()
st.altair_chart(c, use_container_width=True)

"""
### CO2 (Kg)
"""
c = alt.Chart(site_df).mark_circle(size=60, color="#666b73").encode(
    x='date_stamp',
    y='C02 (Kg)',
    color='system_name',
    tooltip=['system_name', 'date_stamp', 'C02 (Kg)']
).interactive()
st.altair_chart(c, use_container_width=True)


"""
## Sortable Data Tables 
"""
site_df
