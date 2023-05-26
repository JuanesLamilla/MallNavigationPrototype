import folium
from folium import plugins
import pandas as pd
import streamlit as st
import os
import json
from streamlit_folium import st_folium

st.title('Mall Navigator Prototype :world_map: :shopping_bags:')

# Set up variables
# ----------------------------------------------------------------------------
STORE_LOCS = 'geodata/mall_data.geojson'
SPM_LOCATION = (53.53096649685565, -113.2936327376925)

store_list = ['Cineplex', 'Ardene', 'Safeway', "Urban Planet", "Dollarama"]
reverse_antpath = False

map_SPM = folium.Map(location = SPM_LOCATION, width = "100%", zoom_start = 17)
# ----------------------------------------------------------------------------


# Set up selection boxes. Remove second location when chosen as the start.
# ----------------------------------------------------------------------------
option_start = st.selectbox(
    'Where are you now?',
    store_list)

end_location = list(store_list)
end_location.remove(option_start)

option_end = st.selectbox(
    'Where would you like to go?',
    end_location)
# ----------------------------------------------------------------------------


# Render stores on the map.
# ----------------------------------------------------------------------------
with open(STORE_LOCS) as f:
    store_polygons = json.load(f)

desired_name_tags = [option_start, option_end]

filtered_features = [feature for feature in store_polygons['features'] if feature['properties']['name'] in desired_name_tags]

for feature in filtered_features:
    folium.GeoJson(feature, 
                   highlight_function= lambda feat: {'fillColor': 'blue'}, 
                   tooltip=folium.features.GeoJsonTooltip(fields=["name", "shop"], 
                                                          aliases=["Name:", "Type:"])).add_to(map_SPM)
# ----------------------------------------------------------------------------


# Render path on the map. 
# ----------------------------------------------------------------------------
ant_file_path = 'geodata/paths/' + option_start.replace(" ", "") + '_' + option_end.replace(" ", "") + '.geojson'
if not os.path.isfile(ant_file_path):        # Flip direction of antpath when start/end locations swap. 
    ant_file_path = 'geodata/paths/' + option_end.replace(" ", "") + '_' + option_start.replace(" ", "") + '.geojson'
    reverse_antpath = True

def switchPosition(coordinate):        # Reverse lat/long in geojson for antpath
    coordinate[0], coordinate[1] = coordinate[1], coordinate[0]
    return coordinate

with open(ant_file_path) as f:
  path_linestring = json.load(f)

for feature in path_linestring['features']:        # Convert linestring to list for antpath
    path = feature['geometry']['coordinates']
finalPath = list(map(switchPosition, path))

if reverse_antpath:
    finalPath.reverse()

folium.plugins.AntPath(finalPath).add_to(map_SPM)
# ----------------------------------------------------------------------------

# Call to render Folium map in Streamlit
st_data = st_folium(map_SPM, width=800, height=800)

st.divider()
st.caption('Choose a start and end location to show the best path through the Sherwood Park Mall to reach your destination.')
st.caption('This proof-of-concept demonstrate how to use **:green[folium]** and **:green[streamlit]** to show geographic information (geojson) dynamically on an interactive dashboard. This page was created entirely in Python.')
st.caption('Similar navigation dashboards can be easily created for hospitals, university campus\'s, and more.')
st.caption('Code can be found on [github](https://github.com/JuanesLamilla/MallNavigationPrototype). You can also check out my [portfolio](https://juaneslamilla.github.io/).')