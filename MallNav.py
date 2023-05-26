import folium
from folium import plugins
import pandas as pd
import streamlit as st

import os
import json

import datetime
from streamlit_folium import st_folium

STORE_LIST = ['Cineplex', 'Food Court', 'Safeway']

UMMlocation = (53.53096649685565, -113.2936327376925)
map_UMM = folium.Map(location = UMMlocation, width = "100%", zoom_start = 17) # max zoom: 18



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