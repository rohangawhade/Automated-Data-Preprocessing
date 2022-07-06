import pandas as pd
import numpy as np
import xgboost
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
# from sklearn.metrics import roc_auc_score

# import matplotlib.pyplot as plt

import pandas as pd
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
# from sklearn.pipeline import make_pipeline
# from sklearn.model_selection import cross_val_score

from sklearn.preprocessing import LabelEncoder
Le = LabelEncoder()


def isCategorical(col, n):
    """ Function to check if a column is contains categorical data """
    l = len(pd.unique(col))
    if((n//l)<(n*0.05)):
      return False
    else:
      return True


def predict_val(X, target, X_pred):
    """ Function to predict the null values for categorical columns """

    var_colums = [c for c in X.columns if c not in [target]]
    
    y = X.loc[:, target]
    X = X.loc[:, var_colums]
    
    colTR = [c for c in X.columns if type(X[c].iloc[0]) == str] # converting only string columns to one hot vectors
    # print(colTR)
    column_trans = make_column_transformer((OneHotEncoder(handle_unknown='ignore'), colTR), remainder='passthrough')
    X = column_trans.fit_transform(X)

    y = Le.fit_transform(y)
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=0)
    # print(X_train.shape, X_valid.shape, y_train.shape, y_valid.shape)

    # Model Training 
    model_xgboost = xgboost.XGBClassifier()

    eval_set = [(X_valid, y_valid)]

    model_xgboost.fit(X_train, y_train, eval_set=eval_set)


    # Model Prediction
    X_pred = X_pred.loc[:, var_colums]
    X_pred = column_trans.transform(X_pred)

    Y_pred = model_xgboost.predict(X_pred)
    print("Predicted values are: ", Y_pred)
    return Le.inverse_transform(Y_pred)