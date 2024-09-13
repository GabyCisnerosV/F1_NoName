##############################################################################
#### F1 Preprocessing
##############################################################################
# This package helps preprocess the data extracted from ERGAST
# In this way the preprocessing for every experiment is done faster and consistently

###########
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Each function does the basic preprocessing used for each dataframe:

def preprocess_F1results(df: pd.DataFrame) -> pd.DataFrame:
    # Turning fastest lap into seconds
    df[['FastestLap.Time.time_MINUTES', 'FastestLap.Time.time_SECONDS']] = df['FastestLap.Time.time'].str.split(":", expand=True)
    df['FastestLap.Time.time_in_seconds'] = df['FastestLap.Time.time_MINUTES'].astype(float) * 60 + df['FastestLap.Time.time_SECONDS'].astype(float)
    df = df.drop(columns=['FastestLap.Time.time_MINUTES', 'FastestLap.Time.time_SECONDS'])
    
    # Creating Season-Round feature
    df["season-round"] = df["season"].astype(str) + "-" + df["round"].astype(str)
    
    # Drop columns
    df = df.drop(columns=['Unnamed: 0.2','Unnamed: 0.1', 'Unnamed: 0'])

    # Encode features
    for i in ['Circuit.circuitId','Constructor.constructorId','Driver.driverId']:
        encoder=LabelEncoder()
        encoder.fit(df[i])
        encoder_values=encoder.transform(df[i])
        name_encoded_feature=i+"_encoded"
        df[name_encoded_feature]=encoder_values

    return df

def preprocess_F1laps(df: pd.DataFrame) -> pd.DataFrame:
    # Transforming lap_duration into seconds
    df[['lap_duration_MINUTES', 'lap_duration_SECONDS', 'EXTRA']] = df['time'].str.split(":", expand=True)
    df['lap_duration_in_seconds'] = df['lap_duration_MINUTES'].astype(float) * 60 + df['lap_duration_SECONDS'].astype(float)
    df = df.drop(columns=['lap_duration_MINUTES', 'lap_duration_SECONDS', 'EXTRA'])
    
    # Drop columns
    df = df.drop(columns=['Unnamed: 0.2','Unnamed: 0.1', 'Unnamed: 0'])

    return df

def preprocess_F1pits(df: pd.DataFrame) -> pd.DataFrame:
    # Transforming pits duration into seconds
    df[['duration_SECONDS', 'EXTRA']] = df['duration'].str.split(":", expand=True)
    df['duration_in_seconds'] = df['duration_SECONDS'].astype(float)
    df = df.drop(columns=['duration_SECONDS', 'EXTRA'])

    # Renaming columns to avoid issues when merging with other dfs
    df=df.rename(columns={"lap":'LapNumber',"time":"pit_stop_time","duration_in_seconds":"pit_stop_duration_in_seconds","stop":"pit_stop_number"})
    
    # Drop columns
    df = df.drop(columns=['Unnamed: 0.2','Unnamed: 0.1', 'Unnamed: 0'])
    
    return df









