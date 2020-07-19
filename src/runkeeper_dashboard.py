import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from typing import List
from datetime import datetime, timedelta
from user_stats import UserStats

import streamlit as st
import pydeck as pdk

# Set values for the below
RUNKEEPER_DATA_LOC = "../runkeeper_data/"

st.title("Runkeeper analysis")

users_file_location = os.path.join(RUNKEEPER_DATA_LOC, "users.csv")
users_df = pd.read_csv(users_file_location)

user_display_names = users_df["display_name"].values

def display_stats_for_selected_user(user_display_name: str):
    user_stats_file_name = users_df[users_df["display_name"] == user_display_name]["file_name"].values[0]
    print(user_stats_file_name)
    user_stats_file_location = os.path.join(RUNKEEPER_DATA_LOC, user_stats_file_name)
    user_stats = UserStats(user_stats_file_location)
    st.text(user_stats.median_speed_for_user)
    st.text(user_stats.median_duration_for_user)
    st.text(user_stats.median_distance_for_user)

    df_grouped_stats_by_day_type = user_stats.get_grouped_user_stats_by_day_type()
    df_grouped_stats_by_start_hour = user_stats.get_grouped_user_stats_by_start_hour()
    st.dataframe(df_grouped_stats_by_day_type)
    st.dataframe(df_grouped_stats_by_start_hour)

    df_filtered_user = user_stats.filtered_by_minimum_duration_user_df
    st.line_chart(df_filtered_user["Distance (km)"])

display_stats_for_selected_user("p1")



