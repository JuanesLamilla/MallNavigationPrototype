import folium
from folium import plugins
import pandas as pd
import streamlit as st

import os
import json

from streamlit_folium import st_folium

store_list = ['Cineplex', 'Ardene', 'Safeway', "Urban Planet", "Dollarama"]
STORE_LOCS = 'geodata/mall_data.geojson'
reverse_antpath = False

SPM_Location = (53.53096649685565, -113.2936327376925)
map_SPM = folium.Map(location = SPM_Location, width = "100%", zoom_start = 17) # max zoom: 18

st.title('Mall Navigator Prototype :world_map: :shopping_bags:')
st.caption('Choose a start and end location to show the best path through the mall to reach your destination.')
st.caption('This proof of concept demonstrate how to use geojson, folium, and a streamlit to show dynamic geographic information on an interactive dashboard. This page was created entirely in Python.')
st.caption('Code can be found on [github](https://github.com/JuanesLamilla/MallNavigationPrototype). You can also check out my [portfolio](https://juaneslamilla.github.io/).')

option_start = st.selectbox(
    'Where are you now?',
    store_list)

end_location = list(store_list)
end_location.remove(option_start)

option_end = st.selectbox(
    'Where would you like to go?',
    end_location)

# render Stores on map
# Load the GeoJSON file
with open(STORE_LOCS) as f:
    data = json.load(f)

# Specify the name tags of the polygons you want to display
desired_name_tags = [option_start, option_end]

# Filter the features based on their properties
filtered_features = [feature for feature in data['features'] if feature['properties']['name'] in desired_name_tags]
# Add the filtered features to the map

for feature in filtered_features:
    folium.GeoJson(feature, highlight_function= lambda feat: {'fillColor': 'blue'}, tooltip=folium.features.GeoJsonTooltip(fields=["name", "shop"], aliases=["Name:", "Type:"])).add_to(map_SPM)


# render path
path_file = 'geodata/paths/' + option_start.replace(" ", "") + '_' + option_end.replace(" ", "") + '.geojson'
if not os.path.isfile(path_file):
    path_file = 'geodata/paths/' + option_end.replace(" ", "") + '_' + option_start.replace(" ", "") + '.geojson'
    reverse_antpath = True

def switchPosition(coordinate):
    coordinate[0], coordinate[1] = coordinate[1], coordinate[0]
    return coordinate

with open(path_file) as f:
  testWay = json.load(f)

for feature in testWay['features']:
    path = feature['geometry']['coordinates']
finalPath = list(map(switchPosition, path))

if reverse_antpath:
    finalPath.reverse()

folium.plugins.AntPath(finalPath).add_to(map_SPM)

# call to render Folium map in Streamlit
st_data = st_folium(map_SPM, width=800, height=800)