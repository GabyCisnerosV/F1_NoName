# 🏎️ F1_Predictor

Hi! My name is Gabriela, and I've been a passionate F1 fan since I was around 10 years old. I'm working on an algorithm to predict who will win the race several laps before it ends. This project is a continuous work in progress as I test different algorithms and paths to reach my goal.

I know predicting a race outcome several laps before it ends (not even mention before it starts) is almost impossible 🥲 There are many factors that influence who wins a race in F1. Some can be predicted easily, while others cannot. Factors like accidents, different weather conditions, and race strategies all play a role. However, it’s worth trying and gaining experience along the way. 💪

## 🚀 What Has Been Done...

1. **Initial Prediction Attempt**: I first tried to get a prediction directly from the features available in the Ergast API. Since some features are not available during the race, the number of features selected for this first attempt was not optimal, resulting in less accurate predictions (file: `3_Model_1.ipynb`).

2. **Predicting Pit Stops**: I decided it would be better to predict different factors of the race first before trying to predict the overall result. Therefore, I attempted to predict the number of pit stops during an F1 race for each driver (file: `Predicting_pitstops.ipynb`).

If you have any suggestions or ideas, please feel free to let me know! 😊

## 📂 Repository Guide:

- `1_API_Requests_Ergast.py`: 📊 Extracts race, qualifying, pit stops, and lap data from the Ergast API.
- `2_EDA_Part1.ipynb`: 📈 Provides initial insights on average speeds, lap times, podiums, and driver performance using Ergast API data.
- `3_Model_1.ipynb`: 🏆 First attempt at predicting the podium directly from the Ergast API data without predicting any intermediate factors.
- `F1_Preprocessing.py`: 🛠️ Contains customized functions to preprocess the data uniformly across the notebooks.
- `Predicting_pitstops.ipynb`: ⛽ Predicts the number of pit stops in a race for each driver.
