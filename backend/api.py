from flask import Flask, request, redirect
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from categorical import isCategorical, predict_val
from continuous import ContinuousPreProcess
from image import processImage
from dotenv import load_dotenv
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
import os
import json
import pyrebase
import time
import pandas as pd

load_dotenv()
UPLOAD_FOLDER = 'D:\\Github Repositories\\Automated-Data-Preprocessing\\backend\\uploads'  # noqa: E501
IMAGE_UPLOAD_FOLDER = 'D:\\Github Repositories\\Automated-Data-Preprocessing\\backend'  # noqa: E501

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "*"}})

config = {
    "apiKey": os.getenv('REACT_APP_API_KEY'),
    "authDomain": os.getenv('REACT_APP_AUTH_DOMAIN'),
    "projectId": os.getenv('REACT_APP_PROJECT_ID'),
    "storageBucket": os.getenv('REACT_APP_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('REACT_APP_MESSAGING_SENDER_ID'),
    "appId": os.getenv('REACT_APP_APP_ID'),
    "measurementId": os.getenv('REACT_APP_MEASUREMENT_ID'),
    "databaseURL": os.getenv("REACT_APP_DATABASE_URL"),
}


@app.route("/upload", methods=['GET', 'POST'])
@cross_origin()
def getDataset():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:
            # If image folder is uploaded
            if file.filename[-4:] == ".zip":
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                imgPath, displayImages = processImage(UPLOAD_FOLDER, filename)

                # Uploading dataset to firebase storage
                firebase_storage = pyrebase.initialize_app(config)
                storage = firebase_storage.storage()
                # print("Storing in firebase")
                fName = filename+str(int(time.time()))+".zip"
                storage.child(fName).put(IMAGE_UPLOAD_FOLDER+"\\"+imgPath)
                # print("Stored in firebase")
                return json.dumps({
                    'success': True,
                    'data': None,
                    'displayImages': json.dumps(displayImages),
                    'ogFileName': file.filename,
                    'nameText': fName,
                    'json_data': None}), 200, {'ContentType': 'application/json'}  # noqa: E501

            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            continuous_processed_path, categorical_processed_path, final_encoded_path = process_data(UPLOAD_FOLDER, filename)  # noqa: E501
            data = pd.read_csv(categorical_processed_path)

            # Uploading dataset to firebase storage
            firebase_storage = pyrebase.initialize_app(config)
            storage = firebase_storage.storage()
            fName = filename+str(int(time.time()))+".csv"
            storage.child(fName).put(final_encoded_path)

            json_data = data.to_json()
            data = data.head(50)
            df = str(data.to_html())
            print(filename+" processed")
            return json.dumps({
                'success': True,
                'data': df,
                'ogFileName': file.filename,
                'nameText': fName,
                'json_data': json_data}), 200, {'ContentType': 'application/json'}  # noqa: E501
    else:
        return json.dumps({
            'success': True,
            'data': "Get Method"}), 200, {'ContentType': 'application/json'}


@app.route("/")
def Home():
    return "Hello"


def process_data(path, filename):
    """
    Function will take the uploaded csv and
    perform Cleaning and return the cleaned CSV
    """
    # Call Continuous data preprocessing
    data = ContinuousPreProcess(path+"\\"+filename)
    data.to_csv(path+"\\"+filename.replace(".csv", "")+"_Continuous_Processed.csv", header=True, index=False)  # noqa: E501
    continuous_processed_path = path+"\\"+filename.replace(".csv", "")+"_Continuous_Processed.csv"  # noqa: E501

    # Call Categorical data preprocessing
    categorical_processed_path, n = process_categorical(path+"\\"+filename.replace(".csv", "")+"_Continuous_Processed.csv", filename)  # noqa: E501
    final_encoded_path = encodeData(categorical_processed_path, n)
    return (continuous_processed_path, categorical_processed_path, final_encoded_path)  # noqa: E501


def process_categorical(path_of_csv, filename):
    """
    Function to process Categorical Data
    """
    df = pd.read_csv(path_of_csv)
    n = len(df.index)

    # finding total number of nulls in each column
    sr = df.isnull().sum()

    # sorting the series in descending order
    # of total number of nulls present in a column
    sr = sr.sort_values(ascending=False)
    df_keys = sr.keys()

    for i in range(len(df_keys)):
        if(sr.get(key=df_keys[i]) == 0):
            break
        if(not isCategorical(df[df_keys[i]], n)):
            continue

        # keeps a track of all rows which do not have any
        # null values except df_keys[i]
        l1 = df.drop([df_keys[i]], axis=1).dropna().index.tolist()

        # keeps a track of all null values in df_keys[i]
        l2 = df[df[df_keys[i]].isnull()].index.tolist()

        l3 = [index for index in l1 if index in l2]
        to_predict = df.loc[l3]

        # predicting the values at the null places
        df_pred = predict_val(df.dropna(), df_keys[i], to_predict)

        df[df_keys[i]].loc[l3] = df_pred
        print(df_keys[i], df_pred)

    df = df.dropna()
    df.to_csv(path_of_csv.replace("_Continuous_Processed.csv", "")+"_Categorical_Processed.csv", header=True, index=False)  # noqa: E501
    return (path_of_csv.replace("_Continuous_Processed.csv", "")+"_Categorical_Processed.csv", n)  # noqa: E501


def encodeData(path_of_csv, n):
    """
    Funtion to encode the CSV file with
    strings to one hot encoded columns
    """

    df = pd.read_csv(path_of_csv)
    only_str = []
    to_remove = []
    n = len(df.index)
    # print(df.columns)
    for i in range(len(df.columns)-1):
        if(type(df[df.columns[i]].iloc[0]) == str):
            only_str.append(df.columns[i])
    # print(only_str)
    for i in only_str:
        if(not isCategorical(df[i], n)):
            to_remove.append(only_str.pop(only_str.index(i)))
    to_remove.append(df.columns[-1])
    # df = df.drop(to_remove, axis = 1)
    column_trans_final = make_column_transformer((OneHotEncoder(
        handle_unknown='ignore'), only_str),
        remainder='passthrough')

    df = column_trans_final.fit_transform(df)
    df = pd.DataFrame(df)
    df = df.dropna()
    df.columns = column_trans_final.get_feature_names()
    df.to_csv(path_of_csv.replace("_Categorical_Processed.csv", "_Final_Encoded.csv"), index=False)  # noqa: E501
    return path_of_csv.replace("_Categorical_Processed.csv", "_Final_Encoded.csv")  # noqa: E501


if __name__ == '__main__':
    app.run()
