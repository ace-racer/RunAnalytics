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
        grouped_df.columns = ["team", "Num. runners"]
        return grouped_df

    @property
    def median_values_across_teams(self) -> pd.DataFrame:
        pass

    @property
    def team_names(self) -> List[str]:
        return self.user_details_df["team"].unique()

    def __init__(self, user_details_file_location: str, base_location: str):
        self.user_details_df = self._get_user_details_from_file(user_details_file_location)
        self.all_user_stats = []
        for itr, row in self.user_details_df.iterrows():
            user_file_name = row["file_name"]
            user_file_location = os.path.join(base_location, user_file_name)
            user_stats = UserStats(user_file_location)
            self.all_user_stats.append(user_stats)




