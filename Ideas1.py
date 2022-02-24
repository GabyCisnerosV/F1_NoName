# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 16:56:41 2022

@author: gabri
"""

#Hola Gaby
#First trial to have F1 data



##############################################################################
#https://ergast.com/mrd/
##############################################################################

import requests

#Data from Results Ergast API
#Documentation https://ergast.com/mrd/methods/results/
response=requests.get("http://ergast.com/api/f1/2021/1/results.json")

print(response.status_code) #200 ok

response.json() #json response


#To continue
#https://ergast.com/mrd/methods/results/