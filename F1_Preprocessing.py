##############################################################################
#### F1 Preprocessing
##############################################################################
# This package helps preprocess the data extracted from ERGAST
# In this way the preprocessing for every experiment is done faster and consistently

###########
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

# Preprocessing for all Ergast DFs

def preprocess_F1_all(df: pd.DataFrame) -> pd.DataFrame:
    # Lower case columns
    df.columns=df.columns.str.lower()
    # Drop columns
    df = df.drop(columns=['unnamed: 0.2','unnamed: 0.1', 'unnamed: 0'])
    return df


# Each function does the basic preprocessing used for each dataframe:

def preprocess_F1results(df: pd.DataFrame) -> pd.DataFrame:
    # Apply preprocessing for all
    df=preprocess_F1_all(df)

    # Turning fastest lap into seconds
    df[['fastestlap.time.time_MINUTES', 'fastestlap.time.time_SECONDS']] = df['fastestlap.time.time'].str.split(":", expand=True)
    df['fastestlap.time.time_in_seconds'] = df['fastestlap.time.time_MINUTES'].astype(float) * 60 + df['fastestlap.time.time_SECONDS'].astype(float)
    df = df.drop(columns=['fastestlap.time.time_MINUTES', 'fastestlap.time.time_SECONDS'])
    
    # Creating Season-Round feature
    df["season-round"] = df["season"].astype(str) + "-" + df["round"].astype(str)

    # Encode features
    for i in ['circuit.circuitid','constructor.constructorid','driver.driverid']:
        encoder=LabelEncoder()
        encoder.fit(df[i])
        encoder_values=encoder.transform(df[i])
        name_encoded_feature=i+"_encoded"
        df[name_encoded_feature]=encoder_values

    return df

def preprocess_F1laps(df: pd.DataFrame) -> pd.DataFrame:
    # Apply preprocessing for all
    df=preprocess_F1_all(df)

    # Transforming lap_duration into seconds
    df[['lap_duration_MINUTES', 'lap_duration_SECONDS', 'EXTRA']] = df['time'].str.split(":", expand=True)
    df['lap_duration_in_seconds'] = df['lap_duration_MINUTES'].astype(float) * 60 + df['lap_duration_SECONDS'].astype(float)
    df = df.drop(columns=['lap_duration_MINUTES', 'lap_duration_SECONDS', 'EXTRA'])

    return df

def preprocess_F1pits(df: pd.DataFrame) -> pd.DataFrame:
    # Apply preprocessing for all
    df=preprocess_F1_all(df)

    # Transforming pits duration into seconds
    df[['duration_SECONDS', 'EXTRA']] = df['duration'].str.split(":", expand=True)
    df['duration_in_seconds'] = df['duration_SECONDS'].astype(float)
    df = df.drop(columns=['duration_SECONDS', 'EXTRA'])

    # Renaming columns to avoid issues when merging with other dfs
    df=df.rename(columns={"lap":'lapnumber',"time":"pit_stop_time","duration_in_seconds":"pit_stop_duration_in_seconds","stop":"pit_stop_number"})

    return df









