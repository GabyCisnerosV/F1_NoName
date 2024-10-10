##############################################################################
#### F1 Preprocessing
##############################################################################
# This package helps preprocess the data extracted from ERGAST
# In this way the preprocessing for every experiment is done faster and consistently

###########
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from dateutil.relativedelta import relativedelta

##############################################################################
# Preprocessing for all Ergast DFs
##############################################################################

def preprocess_F1_all(df: pd.DataFrame) -> pd.DataFrame:
    # Lower case columns
    df.columns=df.columns.str.lower()
    # Drop columns
    df = df.drop(columns=['unnamed: 0.2','unnamed: 0.1', 'unnamed: 0','unnamed: 0.3','unnamed: 0.4','unnamed: 0.5'])
    df = df.drop_duplicates()
    return df

##############################################################################
# Function to change time features to milliseconds
##############################################################################

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

##############################################################################
# Each function does the basic preprocessing used for each dataframe:
##############################################################################

def preprocess_F1results(df: pd.DataFrame, OneHotEncoder=False,HandleNulls=True) -> pd.DataFrame:
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
    
    # Remove leading and trailing spaces in strings
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Creating Season-Round feature
    df["season-round"] = df["season"].astype(str) + "-" + df["round"].astype("str").str.zfill(2)
    df["season-round-driverid"] = df["season"].astype(str) + "-" + df["round"].astype("str").str.zfill(2) + "-" + df["driverid"].astype(str)

    # Create age feature
    df["driver.dateofbirth"]=pd.to_datetime(df["driver.dateofbirth"])
    df["date"]=pd.to_datetime(df["date"])
    df["driver.age_at_race"] =df.apply(lambda row: relativedelta(row["date"], row["driver.dateofbirth"]).years, axis=1)

    # Handling nulls:
    if HandleNulls==True:
        # We see that there are nulls in race_time.millis features, all of them when the final status is not "Finished".
        # Filling these casses with 999 999 999 milliseconds
        for i in ['race_time.millis','fastestlap.rank','fastestlap.lap','fastestlap.time.time','fastestlap.time.in_milliseconds']:
            df[i]=df[i].fillna(999999999)

        #in the following case we need a lower speed to represent when there was no fastest lap average speed
        df['fastestlap.averagespeed.speed']=df['fastestlap.averagespeed.speed'].fillna(0)

    # Create higher level classes for final status
    LapsPlus=['+1 Lap','+10 Laps','+11 Laps','+12 Laps','+14 Laps','+17 Laps','+2 Laps','+26 Laps','+3 Laps','+4 Laps','+42 Laps','+5 Laps','+6 Laps','+7 Laps','+8 Laps','+9 Laps']
    mechanical_issues=['Alternator', 'Battery', 'Brake duct', 'Brakes', 'Broken wing', 'Clutch', 'Collision', 'Collision damage', 'Cooling system', 'Damage', 'Debris','Differential','Driver Seat', 'Driveshaft', 'Drivetrain', 'ERS', 'Electrical', 'Electronics', 'Engine', 'Engine fire', 'Engine misfire','Excluded', 'Exhaust','Fire', 'Front wing', 'Fuel', 'Fuel leak', 'Fuel pressure', 'Fuel pump', 'Fuel rig', 'Fuel system', 'Gearbox', 'Handling', 'Heat shield fire', 'Hydraulics','Launch control', 'Mechanical','Oil leak', 'Oil line', 'Oil pressure', 'Out of fuel', 'Overheating', 'Pneumatics', 'Power Unit','Power loss', 'Puncture', 'Radiator', 'Rear wing', 'Refuelling','Seat', 'Spark plugs', 'Spun off', 'Steering', 'Suspension', 'Technical', 'Throttle', 'Track rod', 'Transmission', 'Turbo', 'Tyre', 'Tyre puncture', 'Undertray', 'Vibrations', 'Water leak', 'Water pressure', 'Water pump', 'Wheel','Wheel nut', 'Wheel rim', 'Withdrew']
    medical_issues=['Illness','Injured','Injury']
    not_classified=['Did not qualify','Not classified']
    df['final_status_grouped']=np.where(df["final_status"].isin(LapsPlus),'+Laps','Other')
    df['final_status_grouped']=np.where(df["final_status"].isin(mechanical_issues),'Mechanical Issues',df['final_status_grouped'])
    df['final_status_grouped']=np.where(df["final_status"].isin(medical_issues),'Medical Issues',df['final_status_grouped'])
    df['final_status_grouped']=np.where(df["final_status"].isin(not_classified),'Not Classified',df['final_status_grouped'])
    df['final_status_grouped']=np.where(df["final_status_grouped"]=='Other',df["final_status"],df['final_status_grouped'])

    # Add features relative to other drivers in the same season-round
    group_Season_round=df.groupby(["season", "round"]).agg(
    race_time_millis_max_round_season=("race_time.millis", "max"),
    race_time_millis_min_round_season=("race_time.millis", "min"),
    race_time_millis_avg_round_season=("race_time.millis", "mean")).reset_index()
    df=df.merge(group_Season_round,on=["season", "round"]) 
    df["race_time_millis_to_max"]=df["race_time.millis"]-df["race_time_millis_max_round_season"]
    df["race_time_millis_to_min"]=df["race_time.millis"]-df["race_time_millis_min_round_season"]
    df["race_time_millis_to_avg"]=df["race_time.millis"]-df["race_time_millis_avg_round_season"]

    # Encode features
    to_encode=['circuit.circuitid','constructor.constructorid','driverid','final_status_grouped']

    if OneHotEncoder==True:
        df = pd.concat([pd.get_dummies(df, columns = to_encode),df[to_encode]],axis=1)

    elif OneHotEncoder==False:
        for i in to_encode:
            encoder=LabelEncoder()
            encoder.fit(df[i])
            encoder_values=encoder.transform(df[i])
            name_encoded_feature=i+"_encoded"
            df[name_encoded_feature]=encoder_values

    df=df.drop(columns=["final_status",'driver.url','driver.permanentnumber',
                        'driver.code','race_time.time','fastestlap.averagespeed.units']) #this features do not add anything in the analysis and cause duplicates

    return df.drop_duplicates()

##############################################################################

def preprocess_F1laps(df: pd.DataFrame) -> pd.DataFrame:
    # Apply preprocessing for all
    df=preprocess_F1_all(df)

    # Change to Milliseconds:
    df['lap_duration_in_miliseconds']=df['lapduration'].apply(lambda x: None if x is None else time_features_to_milliseconds(str(x)))
    
    #rename columns
    df=df.rename(columns={'lapnumber':"current_lap_number",
                          'position':"current_position"})
    
    # Remove leading and trailing spaces in strings
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # drop columns
    df=df.drop(columns=["time"])
    return df.drop_duplicates()

##############################################################################

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

    # Remove leading and trailing spaces in strings
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df.drop_duplicates()

##############################################################################
# Function to convert columns to float where possible
##############################################################################

def convert_to_float(column):
    if pd.api.types.is_numeric_dtype(column):
        return column.astype(float)
    elif pd.api.types.is_string_dtype(column):
        try:
            return column.astype(float)
        except ValueError:
            return column
    else:
        return column
    
##############################################################################
# Function to add a retro view relative to Season-Round
##############################################################################

def get_past_rows(DF,N,iterator_feature,grouper_feature,features_added):
    """
    DF: Base dataframe
    N: number of rows from the past we want in current observation
    iterator_feature: feature by what the df is being iterated (ex: driverid)
    grouper_feature: feature by what the df is being grouped (ex: season-round)
    features_added: features to add on the right
    """
    DF_Result=pd.DataFrame()
    for obs in set(DF[iterator_feature].unique()):
        #ALL DATA
        OBS_DF=DF[DF[iterator_feature]==obs].sort_values(by=grouper_feature).reset_index().drop(columns="index")

        for N_num in range(N):
            #CREATE ANOTHER ONE ADDING N NUMBER OF ROWS ON TOP AND DELETING N AT THE BOTTOM
            empty_rows = pd.DataFrame(columns=OBS_DF.columns, index=list(range(N))[:N_num+1])
            OBS_DF_N = pd.concat([empty_rows, OBS_DF], ignore_index=True)[features_added]
            OBS_DF_N = OBS_DF_N[:len(OBS_DF_N)-N_num-1]
            OBS_DF_N = OBS_DF_N.add_suffix(f'-{N_num+1}')

            #CONCATENATE
            OBS_DF=pd.concat([OBS_DF,OBS_DF_N],axis=1)
        
        #DROP NA ROWS AT THE BEGINNING:
        OBS_DF = OBS_DF[~OBS_DF[OBS_DF_N.columns[-1]].isna()]
        DF_Result=pd.concat([DF_Result,OBS_DF])

    #turn new columns into floats
    DF_Result = DF_Result.apply(convert_to_float)
    return DF_Result







