##############################################################################
#### F1 Preprocessing
##############################################################################
# This package helps preprocess the data extracted from ERGAST
# In this way the preprocessing for every experiment is done faster and consistently

###########
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

###########
# Preprocessing for all Ergast DFs
###########
def preprocess_F1_all(df: pd.DataFrame) -> pd.DataFrame:
    # Lower case columns
    df.columns=df.columns.str.lower()
    # Drop columns
    df = df.drop(columns=['unnamed: 0.2','unnamed: 0.1', 'unnamed: 0'])
    df = df.drop_duplicates()
    return df

###########
# Function to change time features to milliseconds
###########
def time_features_to_milliseconds(time_str: str) -> float:
    # Split time into its components (hours, minutes, seconds.milliseconds)
    parts = time_str.split(':')

    # Initialize time components
    hours, minutes, seconds, milliseconds = 0, 0, 0, 0

    # Based on the number of parts, assign to hours, minutes, seconds
    if len(parts) == 3:  # Format is hours:minutes:seconds.milliseconds
        hours = float(parts[0])
        minutes = float(parts[1])
        seconds_with_ms = parts[2]
    elif len(parts) == 2:  # Format is minutes:seconds.milliseconds
        minutes = float(parts[0])
        seconds_with_ms = parts[1]
    elif len(parts) == 1:  # Format is seconds.milliseconds
        seconds_with_ms = parts[0]

    # Split seconds into seconds and milliseconds if necessary
    if '.' in seconds_with_ms:
        seconds, milliseconds = map(float, seconds_with_ms.split('.'))
    else:
        seconds = float(seconds_with_ms)

    # Convert all parts to milliseconds
    total_milliseconds = (
        hours * 60 * 60 * 1000 +  # Hours to milliseconds
        minutes * 60 * 1000 +     # Minutes to milliseconds
        seconds * 1000 +          # Seconds to milliseconds
        milliseconds              # Add milliseconds
    )

    return total_milliseconds

###########
# Each function does the basic preprocessing used for each dataframe:
###########
def preprocess_F1results(df: pd.DataFrame) -> pd.DataFrame:
    # Apply preprocessing for all
    df=preprocess_F1_all(df)

    # Change to Milliseconds:
    df['fastestlap.time.in_milliseconds']=df['fastestlap.time.time'].apply(lambda x: None if x is None else time_features_to_milliseconds(str(x)))
    
    # Renaming columns to avoid issues when merging with other dfs
    df=df.rename(columns={'number':"driver_number",
                          'position':"final_position",
                          'positiontext':'final_positionText',
                          'points':'final_points',
                          'grid':'final_grid',
                          'laps':'final_laps',
                          'status':'final_status',
                          'time.millis':"race_time.millis",
                          'time.time':"race_time.time",
                          "driver.driverid":"driverid"})

    # Creating Season-Round feature
    df["season-round"] = df["season"].astype(str) + "-" + df["round"].astype(str)

    # Encode features
    for i in ['circuit.circuitid','constructor.constructorid','driverid']:
        encoder=LabelEncoder()
        encoder.fit(df[i])
        encoder_values=encoder.transform(df[i])
        name_encoded_feature=i+"_encoded"
        df[name_encoded_feature]=encoder_values

    return df

def preprocess_F1laps(df: pd.DataFrame) -> pd.DataFrame:
    # Apply preprocessing for all
    df=preprocess_F1_all(df)

    # Change to Milliseconds:
    df['lap_duration_in_miliseconds']=df['lapduration'].apply(lambda x: None if x is None else time_features_to_milliseconds(str(x)))
    
    #rename columns
    df=df.rename(columns={'lapnumber':"current_lap_number",
                          'position':"current_position"})
    
    # drop columns
    df=df.drop(columns=["time"])
    return df


def preprocess_F1pits(df: pd.DataFrame) -> pd.DataFrame:
    # Apply preprocessing for all
    df=preprocess_F1_all(df)

    # Change to Milliseconds:
    df['duration_in_milliseconds']=df['duration'].apply(lambda x: None if x is None else time_features_to_milliseconds(str(x)))
    

    # Renaming columns to avoid issues when merging with other dfs
    df=df.rename(columns={"lap":'pit_stop_lap_number',
                          "time":"pit_stop_time",
                          "duration_in_milliseconds":"pit_stop_duration_in_milliseconds",
                          "duration":"pit_stop_duration",
                          "stop":"pit_stop_number"})

    return df









