##############################################################################
#### F1 Modelling Extra Functions
##############################################################################
# This functions help evaluate the models created in the repo

###########
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

##############################################################################
# Classification: Results after creating model through Grid Search
##############################################################################

def grid_search_show_results(gs,X_df,feature_importance_num_features=10):
    """
    gs: grid search object name.
    X_df: Dependent features DF.
    feature_importance_num_features: Number of features features in the feature importance graph. If 0, feature importance is not shown.
    """
    # Show best estimator and score
    print("Best Estimator: ",gs.best_estimator_)
    print("Best Score: ",gs.best_score_)
    # Save results and model
    cv_results = pd.DataFrame(gs.cv_results_)
    best_model = gs.best_estimator_

    if feature_importance_num_features==0:
        continue

    else:
        # Feature importance for top X features of best model
        importances = best_model.feature_importances_
        indices = np.argsort(importances)[::-1][:feature_importance_num_features]  
        DF_importances=pd.DataFrame({"Features":np.array(X_df.columns)[indices],"Feature Importance":importances[indices]})

        fig, axs= plt.subplots(figsize=(8, 6))
        sns.barplot(x="Feature Importance", y="Features", data=DF_importances, ax=axs)
        axs.set_title("Feature Importance",fontsize=15,fontweight="bold")
        plt.show()

    return cv_results,best_model