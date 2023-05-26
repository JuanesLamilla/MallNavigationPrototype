import folium
from folium import plugins
import pandas as pd
import streamlit as st

import os
import json

import datetime
from streamlit_folium import st_folium

STORE_LIST = ['Cineplex', 'Food Court', 'Safeway', "Urban Planet", "Dollarama"]

UMMlocation = (53.53096649685565, -113.2936327376925)
map_UMM = folium.Map(location = UMMlocation, width = "100%", zoom_start = 17) # max zoom: 18

st.title('Mall Navigator Prototype :world_map: :shopping_bags:')
st.caption('Choose a start and end location to show the best path through the mall to reach your destination.')
st.caption('This proof of concept demonstrate how to use geojson, folium, and a streamlit to show dynamic geographic information on an interactive dashboard.')
st.caption('Code can be found on [github](https://github.com/JuanesLamilla/MallNavigationPrototype). You can also check out my [portfolio](https://juaneslamilla.github.io/).')

option_start = st.selectbox(
    'Where are you now?',
    STORE_LIST)

end_location = list(STORE_LIST)
end_location.remove(option_start)

option_end = st.selectbox(
    'Where would you like to go?',
    end_location)



# call to render Folium map in Streamlit
st_data = st_folium(map_UMM, width=400, height=800)