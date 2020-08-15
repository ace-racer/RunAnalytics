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
    
    user_team_name = users_df[users_df["display_name"] == user_display_name]["team"].values[0]
    st.markdown("## User name: " + user_display_name)
    st.markdown("## Team: " + user_team_name)
    
    user_stats_file_location = os.path.join(RUNKEEPER_DATA_LOC, user_stats_file_name)
    
    user_stats = UserStats(user_stats_file_location)
    
    st.markdown("### Runs from {0} to {1}".format(user_stats.first_latest_run_for_user[0], user_stats.first_latest_run_for_user[1]))
    st.text("Number of runs: " + str(user_stats.total_valid_runs_for_user))
    st.text("Median speed (Km/h): " + str(user_stats.median_speed_for_user))
    st.text("Median duration (HH:mm:ss): " + str(user_stats.median_duration_for_user))
    st.text("Median distance (Km): " + str(user_stats.median_distance_for_user))
    
    # Get the most productive day and start hour based on duration of the run
    df_grouped_stats_by_day_of_week = user_stats.get_grouped_user_stats_by_day_of_week()
    df_grouped_stats_by_start_hour = user_stats.get_grouped_user_stats_by_start_hour()
    
    # Get the most productive day of week
    most_productive_day_metrics = user_stats.get_most_productive_day(df_grouped_stats_by_day_of_week)
    st.text("Most productive day in the week: {0} for metric: {1} with metric value: {2}"\
            .format(most_productive_day_metrics["achieved_at"], most_productive_day_metrics["metric"], most_productive_day_metrics["metric_value"]))
    
    # Get the most productive hour of day
    most_productive_hour_metrics = user_stats.get_most_productive_hour(df_grouped_stats_by_start_hour)
    st.text("Most productive hour of the day: {0} for metric: {1} with metric value: {2}"\
            .format(most_productive_hour_metrics["achieved_at"], most_productive_hour_metrics["metric"], most_productive_hour_metrics["metric_value"]))
    
    st.dataframe(df_grouped_stats_by_day_of_week)
    st.dataframe(df_grouped_stats_by_start_hour)

    df_filtered_user = user_stats.filtered_by_minimum_duration_user_df
    
    st.markdown("### Distance covered across runs")
    st.line_chart(df_filtered_user["Distance (km)"])
    
    st.markdown("### Average speed across runs")
    st.line_chart(df_filtered_user["Average Speed (km/h)"])

def get_users_ordered_descending_by_metric(metric="median_distance"):
    team_stats = TeamStats(users_file_location, RUNKEEPER_DATA_LOC)
    user_details_with_stats_df = team_stats.user_details_with_stats
    user_details_with_stats_df = user_details_with_stats_df.sort_values(by=metric, ascending=False)
    return user_details_with_stats_df["display_name"].values

st.title("Details across teams")
display_stats_across_teams()

ordered_user_display_names = get_users_ordered_descending_by_metric()

st.title("Details of runners")
for user_display_name in ordered_user_display_names:
    display_stats_for_selected_user(user_display_name)



