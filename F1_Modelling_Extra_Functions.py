##############################################################################
#### F1 Modelling Extra Functions
##############################################################################
# This functions help evaluate the models created in the repo

###########
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

##############################################################################
# Classification: Results after creating model through Grid Search
##############################################################################
    # Shows and saves best model
    # Shows best score
    # Saves results in df
    # Shows feature importance in graph if needed
def grid_search_show_results(gs,X_df,feature_importance_num_features=10,figuresize=(8, 6)):
    """
    gs: grid search object name.
    X_df: Dependent features DF.
    feature_importance_num_features: Number of features features in the feature importance graph. If 0, feature importance is not shown.
    figuresize: Size of feature importance figure (width,height)
    """
    # Show best estimator and score
    print("Best Estimator: ",gs.best_estimator_)
    print("Best Score: ",gs.best_score_)
    # Save results and model
    cv_results = pd.DataFrame(gs.cv_results_)
    best_model = gs.best_estimator_

    if feature_importance_num_features==0:
        print("-------------------------------------------------------------------------------------")

    else:
        # Feature importance for top X features of best model
        importances = best_model.feature_importances_
        indices = np.argsort(importances)[::-1][:feature_importance_num_features]  
        DF_importances=pd.DataFrame({"Features":np.array(X_df.columns)[indices],"Feature Importance":importances[indices]})

        fig, axs= plt.subplots(figsize=figuresize)
        sns.barplot(x="Feature Importance", y="Features", data=DF_importances, ax=axs)
        axs.set_title("Feature Importance",fontsize=15,fontweight="bold")
        plt.show()

    return cv_results,best_model



##############################################################################
# Classification: Results after doing a prediction
##############################################################################
    # Creates and plots confusion matrix
    # Shows classification report
def classification_test_results(y_test,y_pred,figuresize=(8,8)):
    """
    y_test: array of true target observations
    y_pred: array of predicted target observations
    figuresize: Size of feature importance figure (width,height)
    """

    # Confusion matrix
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Plot confusion matrix
    sns.set_theme(style="whitegrid", font_scale=0.7,font="DejaVu Sans")
    fig, axs = plt.subplots(figsize=figuresize)
    sns.heatmap(conf_matrix, annot=True, fmt=".0f", linewidths=3, cmap='Purples',
                cbar_kws={"shrink": .9},xticklabels=np.unique(y_test), yticklabels=np.unique(y_test),ax=axs)
    axs.set_xlabel('Predicted Label')
    axs.set_ylabel('True Label')
    axs.set_title('Confusion Matrix',fontsize=18,fontweight='bold')
    plt.show()

    # Classification report to see accuracy by class
    print(classification_report(y_test, y_pred))

    return

##############################################################################
# Classification MLP: Results after doing a prediction
##############################################################################
    # Creates accuracy and loss graphs
def MLP_test_results(history_df,figuresize=(6,6)):
    """
    history_df: df with accuracy and loss features for test and training
    figuresize: Size of feature importance figure (width,height)
    """
    # Plot training & validation accuracy values
    fig, axs= plt.subplots(figsize=figuresize,ncols=2,nrows=1)

    # Accuracy Plot
    axs[0].plot(history_df['accuracy'], label='Train Accuracy')
    axs[0].plot(history_df['val_accuracy'], label='Test Accuracy')
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].legend(loc='best')

    # Loss Plot
    axs[1].plot(history_df['loss'], label='Train Loss')
    axs[1].plot(history_df['val_loss'], label='Test Loss')
    axs[1].set_title('Model Loss')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].legend(loc='best')

    plt.tight_layout()
    plt.show()

    return