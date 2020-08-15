import pandas as pd

def get_duration_in_sec(duration):
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


def get_duration_in_hh_mm_ss(duration_in_sec: float) -> str:
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

def get_minimum_based_on_box_plot(df: pd.DataFrame, field_name: str) -> float:
    Q1 = df[field_name].quantile(0.25)
    Q3 = df[field_name].quantile(0.75)
    IQR = Q3 - Q1
    
    print(IQR)
    
    min_value = Q1 - (1.5 * IQR)
    print(min_value)
    
    return min_value

def format_hour_of_day(hour_of_day: int) -> str:
    if hour_of_day >= 0 and hour_of_day <= 23:
        if hour_of_day >=0 and hour_of_day <= 11:
            return str(hour_of_day) + " AM"
        else:
            return str(hour_of_day) + " PM"

    raise ValueError("The hour of day: {0} is outside of the acceptable range".format(hour_of_day))

def format_day_of_week(day_of_week: int) -> str:
    if day_of_week >=0 and day_of_week <= 6:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return days[day_of_week]
    
    raise ValueError("The day of week: {0} is outside of the acceptable range".format(day_of_week))
