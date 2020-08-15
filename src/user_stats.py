import pandas as pd
import numpy as np

import utils

class UserStats:

    def _get_user_stats_from_file(self, user_stats_file_location: str) -> pd.DataFrame:
        if user_stats_file_location:
            df = pd.read_csv(user_stats_file_location) 
            df = df.drop(columns=["Friend's Tagged", "Notes", "GPX File", "Average Heart Rate (bpm)", "Route Name", "Activity Id", "Type"])

            df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d %H:%M:%S')
            df["date"] = df["Date"].apply(lambda x: x.date())
            df["year"] = df["Date"].apply(lambda x: x.year)
            df["month"] = df["Date"].apply(lambda x: x.month)
            df["day"] = df["Date"].apply(lambda x: x.day)
            df["hour"] = df["Date"].apply(lambda x: x.hour)
            df["minute"] = df["Date"].apply(lambda x: x.minute)
            df = df.drop(columns=["Date"])

            df.set_index('date', inplace=True)
            df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

            # 0 is Monday and 6 is Sunday
            df["day_of_week"] = df.index.weekday
            df["day_type"] = df["day_of_week"].apply(lambda x: "Weekend" if (x==5 or x==6) else "Weekday")
            df["duration_sec"] = df["Duration"].apply(utils.get_duration_in_sec)
            return df
        else:
            raise ValueError("The file at location {0} does not exist".format(user_stats_file_name))

    def get_grouped_user_stats_by_day_of_week(self) -> pd.DataFrame:
        df_grouped_day_of_week = self.filtered_user_df\
        .groupby("day_of_week")[["Distance (km)", "duration_sec", "Average Speed (km/h)", "Climb (m)"]]\
        .agg({"Distance (km)": ["median", "sum", "max"], "duration_sec": ["median", "sum", "max"], "Average Speed (km/h)": ["median", "max"], "Climb (m)": ["median", "max"]})
        df_grouped_day_of_week = df_grouped_day_of_week.reset_index()

        df_grouped_day_of_week[("Duration(HH:MM:SS)", "median")] =  df_grouped_day_of_week[("duration_sec", "median")].apply(utils.get_duration_in_hh_mm_ss)
        df_grouped_day_of_week[("Duration(HH:MM:SS)", "max")] =  df_grouped_day_of_week[("duration_sec", "max")].apply(utils.get_duration_in_hh_mm_ss)
        df_grouped_day_of_week[("Duration(HH:MM:SS)", "total")] =  df_grouped_day_of_week[("duration_sec", "sum")].apply(utils.get_duration_in_hh_mm_ss)


        df_grouped_day_of_week = df_grouped_day_of_week.drop(columns=[("duration_sec", "median"), ("duration_sec", "max"), ("duration_sec", "sum")])
        df_grouped_day_of_week_count = self.filtered_user_df.groupby("day_of_week").size().reset_index()
        df_grouped_day_of_week_count.columns = ['day_of_week', 'num_runs']

        result_df = df_grouped_day_of_week.merge(df_grouped_day_of_week_count, on='day_of_week')
        return result_df


    def get_grouped_user_stats_by_start_hour(self) -> pd.DataFrame:
        df_grouped_hour = self.filtered_user_df.groupby("hour")[["Distance (km)", "duration_sec", "Average Speed (km/h)", "Climb (m)"]].agg({"Distance (km)": ["median", "sum", "max"], "duration_sec": ["median", "sum", "max"], "Average Speed (km/h)": ["median", "max"], "Climb (m)": ["median", "max"]})
        df_grouped_hour = df_grouped_hour.reset_index()

        df_grouped_hour[("Duration(HH:MM:SS)", "median")] =  df_grouped_hour[("duration_sec", "median")].apply(utils.get_duration_in_hh_mm_ss)
        df_grouped_hour[("Duration(HH:MM:SS)", "max")] =  df_grouped_hour[("duration_sec", "max")].apply(utils.get_duration_in_hh_mm_ss)
        df_grouped_hour[("Duration(HH:MM:SS)", "total")] =  df_grouped_hour[("duration_sec", "sum")].apply(utils.get_duration_in_hh_mm_ss)


        df_grouped_hour = df_grouped_hour.drop(columns=[("duration_sec", "median"), ("duration_sec", "max"), ("duration_sec", "sum")])

        df_grouped_hour_count = self.filtered_user_df.groupby("hour").size().reset_index()
        df_grouped_hour_count.columns = ['hour', 'num_runs']
        df_grouped_hour_count.head()

        result_df = df_grouped_hour.merge(df_grouped_hour_count, on='hour')
        result_df = result_df.sort_values('num_runs', ascending=False)
        return result_df


    @property
    def median_speed_for_user(self) -> float:
        return self.user_df["Average Speed (km/h)"].median()

    @property
    def median_duration_for_user(self) -> str:
        return utils.get_duration_in_hh_mm_ss(self.user_df["duration_sec"].median())

    @property
    def median_distance_for_user(self) -> float:
        return round(self.user_df["Distance (km)"].median(),2)

    @property
    def filtered_by_minimum_duration_user_df(self) -> pd.DataFrame:
        return self.filtered_user_df

    @property
    def total_valid_runs_for_user(self) -> int:
        return self.user_df.shape[0]

    @property
    def first_latest_run_for_user(self) -> (str, str):
        first = str(self.user_df.index.min().strftime("%Y-%m-%d"))
        latest = str(self.user_df.index.max().strftime("%Y-%m-%d"))
        return (first, latest)

    def get_most_productive_day(self, grouped_stats_by_day_of_week_df: pd.DataFrame, metric="distance") -> str:
        most_productive_day_of_week = grouped_stats_by_day_of_week_df.loc[grouped_stats_by_day_of_week_df[("Distance (km)", "median")].idxmax()][[("Distance (km)", "median"), "day_of_week"]]
        formatted_day_of_week = utils.format_day_of_week(most_productive_day_of_week["day_of_week"])
        
        return {"metric": metric, "achieved_at": formatted_day_of_week, "metric_value": most_productive_day_of_week[("Distance (km)", "median")]}

    def get_most_productive_hour(self, grouped_user_stats_start_hour_df: pd.DataFrame, metric="distance") -> str:
        most_productive_hour = grouped_user_stats_start_hour_df.loc[grouped_user_stats_start_hour_df[("Distance (km)", "median")].idxmax()][[("Distance (km)", "median"), "hour"]]
        formatted_hour_of_day = utils.format_hour_of_day(most_productive_hour["hour"])
        return {"metric": metric, "achieved_at": formatted_hour_of_day, "metric_value": most_productive_hour[("Distance (km)", "median")]}

    def __init__(self, user_stats_file_location: str):
        self.user_df = self._get_user_stats_from_file(user_stats_file_location)
        self.minimum_duration = utils.get_minimum_based_on_box_plot(self.user_df, "duration_sec")
        self.filtered_user_df = self.user_df[self.user_df["duration_sec"] >= self.minimum_duration]
