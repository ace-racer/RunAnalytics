import pandas as pd
import numpy as np

class UserStats:
    def _get_duration_in_sec(self, duration):
        duration_str = str(duration)
        duration_parts = duration.split(":")
        num_parts = len(duration_parts)
        multiplier = 1
        total_secs = 0
        
        while num_parts > 0:
            total_secs += multiplier * int(duration_parts[num_parts - 1])
            multiplier *= 60
            num_parts -= 1
            
        return total_secs


    def _get_duration_in_hh_mm_ss(self, duration_in_sec: float) -> str:
        duration_in_sec= int(duration_in_sec)
        final_duration = ""
        seconds = duration_in_sec % 60
        minutes = ((duration_in_sec % 3600) - seconds) // 60
        hours = duration_in_sec // 3600
        
        if hours:
            final_duration = str(hours) + ":" + str(minutes) + ":" + str(seconds)
        else:
            final_duration = str(minutes) + ":" + str(seconds)
            
        return final_duration

    def _get_minimum_based_on_box_plot(self, df: pd.DataFrame, field_name: str) -> float:
        Q1 = df[field_name].quantile(0.25)
        Q3 = df[field_name].quantile(0.75)
        IQR = Q3 - Q1
        
        print(IQR)
        
        min_value = Q1 - (1.5 * IQR)
        print(min_value)
        
        return min_value

    def _get_user_stats_from_file(self, user_stats_file_name: str) -> pd.DataFrame:
        if user_stats_file_name:
            df = pd.read_csv(user_stats_file_name) 
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
            df["duration_sec"] = df["Duration"].apply(self._get_duration_in_sec)
            return df
        else:
            raise ValueError("The file at location {0} does not exist".format(user_stats_file_name))

    def get_grouped_user_stats_by_day_type(self) -> pd.DataFrame:
        df_grouped_is_weekend = self.filtered_user_df.groupby("day_type")[["Distance (km)", "duration_sec", "Average Speed (km/h)", "Climb (m)"]].agg({"Distance (km)": ["median", "sum", "max"], "duration_sec": ["median", "sum", "max"], "Average Speed (km/h)": ["median", "max"], "Climb (m)": ["median", "max"]})
        df_grouped_is_weekend = df_grouped_is_weekend.reset_index()

        df_grouped_is_weekend[("Duration(HH:MM:SS)", "median")] =  df_grouped_is_weekend[("duration_sec", "median")].apply(self._get_duration_in_hh_mm_ss)
        df_grouped_is_weekend[("Duration(HH:MM:SS)", "max")] =  df_grouped_is_weekend[("duration_sec", "max")].apply(self._get_duration_in_hh_mm_ss)
        df_grouped_is_weekend[("Duration(HH:MM:SS)", "total")] =  df_grouped_is_weekend[("duration_sec", "sum")].apply(self._get_duration_in_hh_mm_ss)


        df_grouped_is_weekend = df_grouped_is_weekend.drop(columns=[("duration_sec", "median"), ("duration_sec", "max"), ("duration_sec", "sum")])
        df_grouped_is_weekend_count = self.filtered_user_df.groupby("day_type").size().reset_index()
        df_grouped_is_weekend_count.columns = ['day_type', 'num_runs']

        result_df = df_grouped_is_weekend.merge(df_grouped_is_weekend_count, on='day_type')
        return result_df


    def get_grouped_user_stats_by_start_hour(self) -> pd.DataFrame:
        df_grouped_hour = self.filtered_user_df.groupby("hour")[["Distance (km)", "duration_sec", "Average Speed (km/h)", "Climb (m)"]].agg({"Distance (km)": ["median", "sum", "max"], "duration_sec": ["median", "sum", "max"], "Average Speed (km/h)": ["median", "max"], "Climb (m)": ["median", "max"]})
        df_grouped_hour = df_grouped_hour.reset_index()

        df_grouped_hour[("Duration(HH:MM:SS)", "median")] =  df_grouped_hour[("duration_sec", "median")].apply(self._get_duration_in_hh_mm_ss)
        df_grouped_hour[("Duration(HH:MM:SS)", "max")] =  df_grouped_hour[("duration_sec", "max")].apply(self._get_duration_in_hh_mm_ss)
        df_grouped_hour[("Duration(HH:MM:SS)", "total")] =  df_grouped_hour[("duration_sec", "sum")].apply(self._get_duration_in_hh_mm_ss)


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
        return self._get_duration_in_hh_mm_ss(self.user_df["duration_sec"].median())

    @property
    def median_distance_for_user(self) -> float:
        return round(self.user_df["Distance (km)"].median(),2)

    @property
    def filtered_by_minimum_duration_user_df(self) -> pd.DataFrame:
        return self.filtered_user_df

    def __init__(self, user_stats_file_name: str):
        self.user_df = self._get_user_stats_from_file(user_stats_file_name)
        self.minimum_duration = self._get_minimum_based_on_box_plot(self.user_df, "duration_sec")
        self.filtered_user_df = self.user_df[self.user_df["duration_sec"] >= self.minimum_duration]
