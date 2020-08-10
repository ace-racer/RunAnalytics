import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from typing import List
from datetime import datetime, timedelta
from user_stats import UserStats
from team_stats import TeamStats

import streamlit as st
import pydeck as pdk

# Set values for the below
RUNKEEPER_DATA_LOC = "../runkeeper_data/"

st.title("Runkeeper analysis")

users_file_location = os.path.join(RUNKEEPER_DATA_LOC, "users.csv")
users_df = pd.read_csv(users_file_location)

user_display_names = users_df["display_name"].values

def display_stats_across_teams():
    team_stats = TeamStats(users_file_location, RUNKEEPER_DATA_LOC)
    combined_team_stats_df = team_stats.combined_team_stats
    st.dataframe(combined_team_stats_df)

def display_stats_for_selected_user(user_display_name: str):
    user_stats_file_name = users_df[users_df["display_name"] == user_display_name]["file_name"].values[0]
    print(user_stats_file_name)
    user_stats_file_location = os.path.join(RUNKEEPER_DATA_LOC, user_stats_file_name)
    
    user_stats = UserStats(user_stats_file_location)
    

    st.markdown("#### Duration: {0} to {1}".format(user_stats.first_latest_run_for_user[0], user_stats.first_latest_run_for_user[1]))
    st.text("Number of runs: " + str(user_stats.total_valid_runs_for_user))
    st.text("Median speed (Km/h): " + str(user_stats.median_speed_for_user))
    st.text("Median duration (HH:mm:ss): " + str(user_stats.median_duration_for_user))
    st.text("Median distance (Km): " + str(user_stats.median_distance_for_user))
    

    df_grouped_stats_by_day_type = user_stats.get_grouped_user_stats_by_day_type()
    df_grouped_stats_by_start_hour = user_stats.get_grouped_user_stats_by_start_hour()
    st.dataframe(df_grouped_stats_by_day_type)
    st.dataframe(df_grouped_stats_by_start_hour)

    df_filtered_user = user_stats.filtered_by_minimum_duration_user_df
    st.line_chart(df_filtered_user["Distance (km)"])

st.title("Details across teams")
display_stats_across_teams()

st.title("Details of runners")
display_stats_for_selected_user("p1")



