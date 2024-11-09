# 🏎️ F1_Predictor

Hi! My name is Gabriela, and I've been a passionate F1 fan since I was around 10 years old. I'm working on an algorithm to predict who will win the race several laps before it ends. This project is a continuous work in progress as I test different algorithms and paths to reach my goal.

I know predicting a race outcome several laps before it ends (not even mention before it starts) is almost impossible 🥲 There are many factors that influence who wins a race in F1. Some can be predicted easily, while others cannot. Factors like accidents, different weather conditions, and race strategies all play a role. However, it’s worth trying and gaining experience along the way. 💪

## 🚀 What Has Been Done...

### 1. **First Model: Predicting the final positions of a race before it starts**
   
   Initially, I tried predicting the final position of drivers in races using only the features available from the Ergast API before the race (like grid position, driver, circuit, etc.). Since there weren’t many of these features, I added data to each observation from past races for each driver to give futher information regarding the drivers performance (like their final position in the previous race, grid position in the previus race, % time difference from average race time (previous race), etc.).
   
   I tried different setups, like using different timeframes of data to train the model (from the last 5-10 seasons), trying different number of past races data added to each row, testing different features from past data, experimenting with various models and hyperparameters using cross-validation (such as Random Forest Classifier and XGBoost), and applying dimensionality reduction techniques (PCA). Despite this, the best overall accuracy I got was 17% (with an F1 score of 15%) during the test phase. However, the predictions were better for higher finishing positions. For instance, the model predicted finishing the race in first position with a precision of 36%, a recall of 53%, and an F1 score of 43%.
   
   It’s important to note that the models tended to overfit, so I applied measures like cross-validation, ensemble methods (bagging and boosting), and simplifying the models to address this. The file related to this analysis is `3_Model_1_PredictingFinalPositions.ipynb`.

   Final thoughts: Using just data like past final positions, final grid , driver, circuit, etc, is not enough to have accurate predictions on the final positions in a race. In the next attempt we try to add more features predicted and from other sources.

### 2. **Predicting Pit Stops: Predicting the number of pit stops per driver per race**

   I decided it would be better to predict different factors of the race first before trying to predict the overall result. Therefore, I attempted to predict the number of pit stops during an F1 race for each driver (file: `3_Model_2_PredictingPitStops.ipynb`).
   
   First, I attempted to predict the number of pit stops in a race based on pre-race data, including information about drivers, constructors, circuits, weather, and tire compounds. I tested several models (and hyperparameters using cross validation), including Random Forest Classifier (with and without PCA), SVMs, XGBoost, and a Multilayer Perceptron.

   One of the challenges I faced during this exercise was overfitting, particularly in models like the MLP. To address this, I used cross-validation, experimented with simpler structures (such as fewer layers and neurons), and included dropout layers to regularize the model. The second challenge I faced was the class imbalance in the target variable (ex: the average number of pit stops per driver in the 2024 season was 1.4). This imbalance led to the models being biased toward predicting less pit stops (1). For this reason, I evaluated the models not only with accuracy but also with the F1 score.

   The best results I got were a general test F1 score of 38% and a test accuracy of 59%. However, the models performed better depending on the number of pit stops, reaching a test F1 score of 68% when predicting 1 pit stop and 46% when predicting 2 pit stops. This suggests that while there is room for improvement predicting a higher number of pit stops, the models capture the most common pit stop behavior relatively good.

### 3. **Predicting when a car will have a Pit Stops: Predicting the laps in which the drivers are going to stop for a pit stop**
   
If you have any suggestions or ideas, please feel free to let me know! 😊

## 📂 Repository Guide:

- `1_API_Requests_Ergast.py`: 📊 Extracts race, qualifying, pit stops, and lap data from the Ergast API.
- `1_API_Requests_FastF1.py`: 🌤️ Extracts data related to laps and weather from FastF1 API.
- `2_EDA_Part1.ipynb`: 📈 Provides initial insights on average speeds, lap times, podiums, and driver performance using Ergast API data.
- `2_EDA_Part2.ipynb`: 🛞 Insights focused on pit stops and related features like weather and compounds. Data from Ergast API and FastF1 API.
- `3_Model_1_PredictingFinalPositions.ipynb`: 🏆 First attempt at predicting the podium directly from the Ergast API data only available before the race.
- `3_Model_2_PredictingPitStops.ipynb`: ⛽ Predicts the number of pit stops in a race for each driver.
- `F1_Preprocessing.py`: 🛠️ Contains customized functions to preprocess the data uniformly across the notebooks.
- `F1_Modelling_Extra_Functions.py`: ⚙️ Contains customized functions to evaluate models.

