# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 16:56:41 2022

@author: gabri
"""





##############################################################################
#f1 Ideas
##############################################################################

import requests
import pandas as pd

path = 'C:/Users/gabri/Dropbox/Gaby/Proyectos/My_Portafolio/F1/Data/'


# ResultsDF.to_csv(path+"ResultsDF.csv")
# QualifyingDF.to_csv(path+"QualifyingDF.csv")
# LapsDF.to_csv(path+"LapsDF.csv")
# PitsDF.to_csv(path+"PitsDF.csv")


# ResultsDF = pd.concat([ResultsDF, df], axis=0)


#ResultsDF.info()
#ResultsDF.groupby("position")["number"].count()






########################I1
#To replace outliers in F1
#Treating outliers with method based on percentiles and caps (1,99)
Laps_Pits_Results['lap_duration_in_seconds_no_outliers']=Laps_Pits_Results['lap_duration_in_seconds'].copy(deep=True)
Years=Laps_Pits_Results["season"].unique().tolist() #or seasons for plot
for y in Years:
    seasoncircuits=Laps_Pits_Results[Laps_Pits_Results["season"]==y]['Circuit.circuitId'].unique().tolist()
    for seascirc in seasoncircuits:
        Cond_A=(Laps_Pits_Results["status"]=="Finished")
        Cond_B=(Laps_Pits_Results["season"]==y)
        Cond_C=(Laps_Pits_Results['Circuit.circuitId']==seascirc)
        Data_with_conditions=Laps_Pits_Results[Cond_A & Cond_B & Cond_C]

        #Quantile measures and caps
        q1=Laps_Pits_Results[Cond_A & Cond_B & Cond_C]['lap_duration_in_seconds_no_outliers'].quantile(0.01)
        q99=Laps_Pits_Results[Cond_A & Cond_B & Cond_C]['lap_duration_in_seconds_no_outliers'].quantile(0.99)

        #Values that are above the limit
        Upper=Data_with_conditions[Data_with_conditions['lap_duration_in_seconds_no_outliers']>q99]['lap_duration_in_seconds_no_outliers']
        Lower=Data_with_conditions[Data_with_conditions['lap_duration_in_seconds_no_outliers']<q1]['lap_duration_in_seconds_no_outliers']

        #Replacing outliers
        for i in Upper:
            Laps_Pits_Results['lap_duration_in_seconds_no_outliers']=Laps_Pits_Results[Cond_A & Cond_B & Cond_C]['lap_duration_in_seconds_no_outliers'].replace(i,q99)

        for i in Lower:
            Laps_Pits_Results['lap_duration_in_seconds_no_outliers']=Laps_Pits_Results[Cond_A & Cond_B & Cond_C]['lap_duration_in_seconds_no_outliers'].replace(i,q1)



#########################I2
#DO PLOT AVERAGE DURATION OF EACH LAP IN A RACE