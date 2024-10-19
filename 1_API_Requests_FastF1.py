
##############################################################################
#### 1_API_REQUESTS_FASTF1
##############################################################################
# Get data regarding laps, compounds, etc
##############################################################################
# f1 Results from https://docs.fastf1.dev/index.html
##############################################################################

import fastf1
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

y_start, y_end = 2014, 2025  # Range of years
r_start, r_end = 1, 30  # Range of races in each year

##############################################################################
### Dataframes I want to store:
WeatherData= pd.DataFrame()
LapsData= pd.DataFrame()

##############################################################################
### Function to get data
def getting_session_data(year, race, event):
    try:
        session = fastf1.get_session(year, race, event)
        session.load(telemetry=False, laps=True, weather=True)
        result = {}

        # Get data if it exists for this race,year,event
        if session.weather_data is not None:
            weather = session.weather_data.copy()
            weather["season"] = year
            weather["session"] = race
            weather["event"] = event
            #to all data dictionary
            result['weather'] = weather

        if session.laps is not None:
            laps = session.laps.copy()
            laps["season"] = year
            laps["session"] = race
            laps["event"] = event
            #to all data dictionary
            result['laps'] = laps

        print(f">>>> Season {year} - Race {race}: {event} data extracted.")
        return result
    
    except Exception as e:
        print(f">>>> Season {year} - Race {race}: {event} data extraction failed due to: {e}")
        return None

##############################################################################
###  Extract data in parallel
with ThreadPoolExecutor(max_workers=1) as executor:
    future_to_session = {executor.submit(getting_session_data, year, race, event): (year, race, event)
                         for year in range(y_start, y_end)
                         for race in range(r_start, r_end)
                         for event in ['Race', 'Practice 1', 'Practice 2', 'Practice 3', 'Sprint', 'Sprint Shootout', 'Sprint Qualifying', 'Qualifying']} #
    # Collect results as they complete
    for future in as_completed(future_to_session):
        session_data = future.result()
        if session_data is not None:
            if 'weather' in session_data:
                WeatherData=pd.concat([WeatherData,session_data['weather']])
            if 'laps' in session_data:
                LapsData=pd.concat([LapsData,session_data['laps']])


# Display summaries of the data
print(f"Total weather records: {len(WeatherData)}")
print(f"Total laps records: {len(LapsData)}")


##############################################################################
### Update Existing files

# Check stored data
path = 'C:/Users/gabri/Dropbox/Gaby/Proyectos/My_Portafolio/F1/Data/'
weather_file = path + "FASTF1_Weather.csv"
laps_file = path + "FASTF1_Laps.csv"
weather_pre, laps_pre= pd.DataFrame(), pd.DataFrame()

# # #check if files are alredy stored or this are the first files
# weather_pre = pd.read_csv(weather_file)
# laps_pre = pd.read_csv(laps_file)

# # Updating or creating dfs
# if weather_pre is not None:
#     weather_updated = pd.concat([WeatherData, weather_pre]).drop_duplicates()
# else:
#     weather_updated = WeatherData

# if laps_pre is not None:
#     laps_updated = pd.concat([LapsData, laps_pre]).drop_duplicates()
# else:
#     laps_updated = LapsData

# # Check changes
# dfs={"Weather Before:":weather_pre,
#      "Laps Before:":laps_pre,
#      "Weather After:":weather_updated,
#      "Laps After:":laps_updated}
# for k,v in dfs.items():
#     print(k,len(v))

# # Save updated dataframes to CSV
# weather_updated.to_csv(weather_file, index=False)
# laps_updated.to_csv(laps_file, index=False)

WeatherData.to_csv(weather_file, index=False)
LapsData.to_csv(laps_file, index=False)
