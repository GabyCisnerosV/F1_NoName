# 🏎️ F1_Predictor

Hi! My name is Gabriela, and I've been a passionate F1 fan since I was around 10 years old. I'm working on an algorithm to predict who will win the race several laps before it ends. This project is a continuous work in progress as I test different algorithms and paths to reach my goal.

I know predicting a race outcome several laps before it ends (not even mention before it starts) is almost impossible 🥲 There are many factors that influence who wins a race in F1. Some can be predicted easily, while others cannot. Factors like accidents, different weather conditions, and race strategies all play a role. However, it’s worth trying and gaining experience along the way. 💪

## 🚀 What Has Been Done...

1. **First Model: Predicting the final positions of a race before it starts**:
   
   Initially, I tried predicting the final position of drivers in races using only the features available from the Ergast API before the race (like grid position, driver, circuit, etc.). Since there weren’t many of these features, I added data to each observation from past races for each driver to give futher information regarding the drivers performance (like their final position in the previous race, grid position in the previus race, % time difference from average race time (previous race), etc.).
   
   I tried different setups, like using different timeframes of data to train the model (from the last 5 or 10 seasons), trying different number of past races data added to each row, testing different features from past data, using different models (Random Forest Classifier and XGBoost), and applying dimensionality reduction techniques (PCA). Despite this, the best overall accuracy I got was 16% (with an F1 score of 15%) during the test phase. However, the predictions were better for higher finishing positions. For instance, the model predicted finishing the race in first position with a precision of 47%, a recall of 50%, and an F1 score of 49%.
   
   It’s important to note that the models tended to overfit, so I applied measures like cross-validation, ensemble methods (bagging and boosting), and simplifying the models to address this. The file related to this analysis is `3_Model_1.ipynb`.

5. **Predicting Pit Stops**: I decided it would be better to predict different factors of the race first before trying to predict the overall result. Therefore, I attempted to predict the number of pit stops during an F1 race for each driver (file: `Predicting_pitstops.ipynb`).

If you have any suggestions or ideas, please feel free to let me know! 😊

## 📂 Repository Guide:

- `1_API_Requests_Ergast.py`: 📊 Extracts race, qualifying, pit stops, and lap data from the Ergast API.
- `2_EDA_Part1.ipynb`: 📈 Provides initial insights on average speeds, lap times, podiums, and driver performance using Ergast API data.
- `3_Model_1.ipynb`: 🏆 First attempt at predicting the podium directly from the Ergast API data only available before the race.
- `F1_Preprocessing.py`: 🛠️ Contains customized functions to preprocess the data uniformly across the notebooks.
- `F1_Modelling_Extra_Functions.py`: ⚙️ Contains customized functions to evaluate models.
- `Predicting_pitstops.ipynb`: ⛽ Predicts the number of pit stops in a race for each driver.
