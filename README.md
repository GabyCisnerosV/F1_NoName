# F1_PredictingPodiumAlgorithm

My name is Gabriela, and I follow F1 since I was around 10 years old. I am looking for an algorithm that helps me predict who will win the race several laps before it ends. This is a project in continuous progress as I am testing different algorithms to find the one that is closer to help me make my predictions

It is difficult, I know! :O
There are a lot of factors that influence who wins a race in F1. Some of them can be predicted easily but some of them cannot.

## What has been done...

First, I tried to get a prediction directly from the features available in the Ergast API. As in the race there are several features that at the moment of the race we don't have available, the number of features selected for this first attempt were not the optimal, so the results were not optimal neither (file: Model.ipynb).

After this, I decided that it was better to predict some different factors of the race first, before trying to predict the whole result. For this resaon I attempted to predict the number of pit stops during an F1 race for each driver (file: Predicting_pitstops.ipynb)

If you have a suggestion or an idea, please feel free to let me know ;)


## Repository Guide:

  1_API_Requests_Ergast.py: File that extracts race, qualifying, pit stops and lap data from Ergast API.
  
  Ideas1.py: A space to write ideas.
  
  Model.ipynb: First attempt of predicting the podium directly from the information obtained, whitout predicting anything before.
 
  Predicting_pitstops.ipynb: Predicnting the number of pitstops in a race for each driver.
  


