# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 16:56:41 2022

@author: gabri
"""





##############################################################################
#f1 Results from https://ergast.com/mrd/
##############################################################################

import requests
import pandas as pd

###
#Individual Test to download Results Database
###

#Data from Results Ergast API
#Documentation https://ergast.com/mrd/methods/results/
Results=requests.get("http://ergast.com/api/f1/2022/18/results.json")
print(Results.status_code) #200 ok
Results.json() #json response
type(Results.json()) #dict

Results=Results.json()
Races=Results['MRData']['RaceTable']["Races"]

df1 = pd.json_normalize(Races,record_path=['Results'],
                       meta=["season","round",'raceName',
                             ['Circuit','circuitId'],
                             ['Circuit','circuitName'],
                             ['Circuit','Location','country']])



###
#Downloading data from 2001 until the last race
###

#1 Results in one table (all but the last race)

ResultsDF=pd.DataFrame()

for year in range(2001,2022): #From 2001 until 2022 (to be able to use in the close future)
    for race in range(1,30): #The maximum number of races was in 2021 with 22 races
        url="http://ergast.com/api/f1/"+str(year)+"/"+str(race)+"/results.json" #modifying the url
        Results=requests.get(url) #Request from API
        Results=Results.json() #Results in json format
        Races=Results['MRData']['RaceTable']["Races"] #subset of desired features
        
        #Each season has a different number of races per year
        if Races!=[]: #if the year and number of race exist
            print("Season ",year,"- Race ",race,": The race was held.")
            df= pd.json_normalize(Races,record_path=['Results'],
                       meta=["season","round",'raceName',
                             ['Circuit','circuitId'],
                             ['Circuit','circuitName'],
                             ['Circuit','Location','country']])
            ResultsDF = pd.concat([ResultsDF, df], axis=0)
        elif Races==[]: #if this number of race was not held that year
            print("Season ",year,"- Race ",race,": The race was NOT held.")
            continue
        
#2 The last race url has a different format:
url="http://ergast.com/api/f1/current/last/results.json" #modifying the url
Results=requests.get(url) #Request from API
Results=Results.json() #Results in json format
Races=Results['MRData']['RaceTable']["Races"] #subset of desired features   
df= pd.json_normalize(Races,record_path=['Results'],
                       meta=["season","round",'raceName',
                             ['Circuit','circuitId'],
                             ['Circuit','circuitName'],
                             ['Circuit','Location','country']])
ResultsDF = pd.concat([ResultsDF, df], axis=0)









response=requests.get("http://ergast.com/api/f1/results.json")
"http://ergast.com/api/f1/2021/1/results.json"

print(response.status_code) #200 ok

response.json() #json response

type(response.json()) #dict


Results=response.json()
Races=Results['MRData']['RaceTable']["Races"]
Races
import pandas as pd

df = pd.json_normalize(Races,record_path=['Results'],
                       meta=["season","round",'raceName',
                             ['Circuit','circuitId'],
                             ['Circuit','circuitName'],
                             ['Circuit','Location','country']])
df.head()







url = "http://ergast.com/api/f1/2021/1/results.json"
df = pd.read_json(url)
print(df)

df=pd.read_json(response.json())
df

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())

#To continue
#https://ergast.com/mrd/methods/results/
#https://www.dataquest.io/blog/python-api-tutorial/



#que factor influye a que haya mas cambio s de llantas en cada carrera
#relacion accidentes y halo
#datos de pretemporada te dicen algo