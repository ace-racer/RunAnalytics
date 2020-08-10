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