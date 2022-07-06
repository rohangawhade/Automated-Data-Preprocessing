#!/usr/bin/env python
from fancyimpute import IterativeImputer
from sklearn.preprocessing import RobustScaler
# from sklearn.neighbors import LocalOutlierFactor
import pandas as pd
import re


def checkNumeric(num):
    if num == num:
        return True if re.search("[0-9]+.*[0-9]*", num) else False
    else:
        return False


def convertToNumeric(data, col):
    for k in range(len(data[col])):
        res = ""
        for i in data[col][k]:
            res += re.sub("[`~!@#$=+%^&*_/?()-]|[a-zA-Z]", "", i)
        res = float(res)
        data.loc[k, col] = res


def CheckUnique(data):
    col_names = data.columns.to_list()
    # print("Original Column Names")
    # print(col_names)
    new_col = col_names.copy()
    for i in col_names:
        if data[i].count() == len(data[i].unique()):
            isUniq = True
        else:
            isUniq = False
        if isUniq:
            # print("Dropping", i)
            new_col.remove(i)
    return new_col


def GetNumColumns(data):
    col_names = data.columns.to_list()
    final_col_names = col_names.copy()
    for i in col_names:
        if data.dtypes[i] == "float" or data.dtypes[i] == "int64" or data.dtypes[i] == "int32":  # noqa: E501
            # print("ALREADY NUMERIC:-", i)
            continue
        else:
            c = 0
            ct = []
            ct.append(data[i][:50])
            for j in ct[0]:
                if checkNumeric(j):
                    c = c+1
            if c > 40:
                # print("Numeric:-", i)
                convertToNumeric(data, i)
                # print("Converted Values of", i)
            else:
                final_col_names.remove(i)
                # print("Not a Numeric:-", i)
            # print("-----------")
    # print("These are the final numeric columns", final_col_names)
    return final_col_names


'''
Scaling / Normalization
In order to identify scale the data, we cannot use the usual scaling methods
such as Min Max Scaler or Logarithmic Scaler because they will consider
outliers into the data and scale accordingly.
Therefore we use a Robust Scaling method where we find the interquartile range
and scale according to the range so that the data is not affected by outliers.
'''


def Scaling(data):
    sc = RobustScaler()
    final_col_names = GetNumColumns(data)
    df = data.copy()
    features = data[final_col_names]
    df[final_col_names] = sc.fit_transform(features.values)
    return df


'''
3. Outlier Analysis
The local outlier factor, or LOF for short, is a technique that attempts
to harness the idea of nearest neighbors for outlier detection.
The IQR can be used to identify outliers by defining limits on the sample
values that are a factor k of the IQR below the 25th percentile or
above the 75th percentile. The common value for the factor k is the value 1.5
'''


def remove_outlier(DF, col_name):
    q1 = DF[col_name].quantile(0.25)
    q3 = DF[col_name].quantile(0.75)
    # print("25th Percentile of Numerical Attributes")
    # print(q1)
    # print("----------------------------")
    # print("75th Percentile of Numerical Attributes")
    # print(q3)
    # print("----------------------------")
    IQR = q3-q1  # Interquartile range
    # print("Interquartile Range")
    # print(IQR)
    d = DF[~((DF[col_name] < (q1 - 1.5 * IQR)) | (DF[col_name] > (q3 + 1.5 * IQR))).any(axis=1)]  # noqa: E501
    return d


def OutlierAnalysis(path):
    data = pd.read_csv(path)  # Reading dataset
    # print("----------------------------")
    # print("Original Dataset ")
    # print("----------------------------")
    # print(data)
    # print("----------------------------")
    col_name = CheckUnique(data)  # Removing unique columns
    data = data[col_name]  # Columns names which are not unique

    # print("----------------------------")
    # print("Count of null values in continuous attributes")
    # print(data.isna().sum())
    cols = GetNumColumns(data)  # get numerical columns
    mice_imputer = IterativeImputer()
    df2 = mice_imputer.fit_transform(data[cols])
    dd = {}
    for i in range(len(cols)):
        dd[cols[i]] = df2[:, i].tolist()
    df4 = pd.DataFrame(dd)
    data[cols] = df4[cols]

    # print("----------------------------")
    # print("Count of null values AFTER removal in continuous attributes")
    # print(data.isna().sum())
    # data2 = data[cols]
    # print("----------------------------")
    # print("Data shape", data.shape)
    # print("Copied Data shape", data2.shape)

    '''
    lof = LocalOutlierFactor()
    yhat = lof.fit_predict(data2.values)  # LOF outlier remover
    mask = yhat != -1
    DF = data[mask]
    print("New Data shape", DF.shape)
    print("----------------------------")
    dd = DF.copy()
    dd = remove_outlier(DF, cols)  # Quartile outlier remover
    '''
    data = Scaling(data)  # Scaling Dataset
    dd = remove_outlier(data, cols)  # Removing outliers after scaling
    return dd


def ContinuousPreProcess(path):
    final_data = OutlierAnalysis(path)
    # print("----------------------------")
    # print("Processed Dataset:")
    # print("----------------------------")
    return final_data
