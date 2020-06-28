import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List
from datetime import datetime, timedelta

import streamlit as st
import pydeck as pdk

st.title("Runkeeper analysis")

column_names = ["run_id", "start_lon", "start_lat", "end_lon", "end_lat", "distance_km", "average_speed_kmph", "time_taken_min"]
runs_df = pd.DataFrame(columns=column_names)
print(runs_df)

def display_runs_across_singapore(runs_df : pd.DataFrame):
    processed_runs_df = runs_df.rename(columns = {'start_lon':'lon', 'start_lat':'lat'})

    # Any value with NA leads to a strange error on the UI
    # No value that are in the DF must not be empty for the map to work
    processed_runs_df = processed_runs_df[["lat", "lon"]]
    midpoint = 1.38, 103.8

    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[	
            pdk.Layer(	
                "HexagonLayer",	
                data=processed_runs_df,
                get_position=["lon", "lat"],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True
            ),	
        ]   
    ))


def display_runs_metrics_compared_to_others():
    pass


def get_potential_distance_based_on_current_runs():
    pass

def get_probable_time_required_to_reach_distance_goal(distance_goal:int) -> int:
    pass

display_runs_across_singapore(runs_df)