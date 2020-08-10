import pandas as pd
import numpy as np
from typing import List
import os

from user_stats import UserStats
import utils

class TeamStats:

    def _get_user_details_from_file(self, user_details_file_location: str) -> pd.DataFrame:
        return pd.read_csv(user_details_file_location)

    @property
    def num_runners_across_teams(self) -> pd.DataFrame:
        grouped_df = self.user_details_df.groupby("team")["display_name"].count().reset_index()
        grouped_df.columns = ["team", "# runners"]
        return grouped_df

    @property
    def median_values_across_teams(self) -> pd.DataFrame:
        grouped_df = self.all_user_details_stats.groupby("team")[["total_runs", "median_speed", "median_distance", "median_duration"]].median()
        grouped_df = grouped_df.reset_index()
        grouped_df["median_duration"] = grouped_df["median_duration"].apply(utils.get_duration_in_hh_mm_ss)
        grouped_df.columns = ["team", "Median # runs", "Median speed (Km/h)", "Median distance (Km)", "Median Duration (HH:mm:ss)"]
        return grouped_df

    @property
    def combined_team_stats(self) -> pd.DataFrame:
        num_runners_df = self.num_runners_across_teams
        median_values_df = self.median_values_across_teams
        merged_df = num_runners_df.merge(median_values_df, on="team")
        return merged_df

    @property
    def user_details_with_stats(self) -> pd.DataFrame:
        return self.all_user_details_stats


    @property
    def team_names(self) -> List[str]:
        return self.user_details_df["team"].unique()

    def __init__(self, user_details_file_location: str, base_location: str):
        self.user_details_df = self._get_user_details_from_file(user_details_file_location)
        dfs = []
        
        for itr, row in self.user_details_df.iterrows():
            user_file_name = row["file_name"]
            user_file_location = os.path.join(base_location, user_file_name)
            user_stats = UserStats(user_file_location)
            
            user_details_stats = {
                "display_name": row["display_name"],
                "team": row["team"],
                "total_runs": user_stats.total_valid_runs_for_user,
                "median_speed": user_stats.median_speed_for_user,
                "median_distance": user_stats.median_distance_for_user,
                "median_duration": utils.get_duration_in_sec(user_stats.median_duration_for_user)
            }

            current_user_details_stats_df = pd.DataFrame(user_details_stats, index=[0])
            dfs.append(current_user_details_stats_df)
        
        self.all_user_details_stats = pd.concat(dfs)




