# from traceback import print_tb
from flask import Flask, request, redirect
# from flask_mail import Mail,Message
from flask_cors import CORS, cross_origin
# from numpy.core.numeric import full_like
# from pymysql import NULL
from werkzeug.utils import secure_filename
from categorical import *
from continuous import *
from image import *
from dotenv import load_dotenv
import os
import json
import pyrebase
import time
import numpy as np
# import pickle

import pandas as pd
# import evalml
# from evalml.automl import AutoMLSearch
# # import pyrebase
# from sklearn.model_selection import train_test_split
# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import f_classif
# from matplotlib import pyplot
# from sklearn.preprocessing import StandardScaler 
# from sklearn.svm import SVC 
# from sklearn.linear_model import LogisticRegression
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.linear_model import LinearRegression
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.svm import SVR
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.model_selection import cross_val_score 



load_dotenv()
UPLOAD_FOLDER = 'D:\\Github Repositories\\Automated-Data-Preprocessing\\backend\\uploads'
IMAGE_UPLOAD_FOLDER = 'D:\\Github Repositories\\Automated-Data-Preprocessing\\backend'

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
    "serviceAccount": "firebase-adminsdk.json",
}

# with open('config.json', 'r') as c:
#     params = json.load(c)["params"]


# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail-user'],
#     MAIL_PASSWORD=  params['gmail-password']
# )
# mail = Mail(app)


@app.route("/upload", methods=['GET', 'POST'])
@cross_origin()
def getDataset():
    print("INSIDEEEEEEEEEEEEEE")
    print(request)
    if request.method == 'POST':
        print("request*****************************")
        if 'file' not in request.files:
            print('no file')
            print("############################################")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("(((((((((((((((((((((((((((((((((((((((((((((((")
            print('no filename')
            return redirect(request.url)
        else:
            print("FILE NAME : ", file.filename)
            # If image folder is uploaded
            if file.filename[-4:] == ".zip":
                filename = secure_filename(file.filename)
                print("PATHHHH = ", os.getcwd())
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                print("saved file successfully")
                imgPath, displayImages = processImage(UPLOAD_FOLDER, filename)
                print("Image path is equal to this: ", imgPath)

                # Uploading dataset to firebase storage
                firebase_storage = pyrebase.initialize_app(config)
                storage = firebase_storage.storage()
                # print(storage.list_files())
                # for i in storage.list_files():
                #     print(storage.child(i.name))
                print("Storing in firebase")
                fName = filename+str(int(time.time()))+".zip"
                storage.child(fName).put(IMAGE_UPLOAD_FOLDER+"\\"+imgPath)
                print("Stored in firebase")
                # numpyData = {"array": displayImages}
                # return json.dumps({'success':True, 'data': "Image zip was successfully uploaded"}), 200, {'ContentType':'application/json'}
                return json.dumps({'success':True, 'data': None, 'displayImages': json.dumps(displayImages), 'ogFileName': file.filename, 'nameText': fName, 'json_data': None }), 200, {'ContentType':'application/json'}

            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            filename = secure_filename(file.filename)
            print("PATHHHH = ", os.getcwd())
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            print("saved file successfully")
            continuous_processed_path, categorical_processed_path, final_encoded_path = process_data(UPLOAD_FOLDER, filename)
            data=pd.read_csv(categorical_processed_path)

            # Uploading dataset to firebase storage
            firebase_storage = pyrebase.initialize_app(config)
            storage = firebase_storage.storage()
            # print(storage.list_files())
            # for i in storage.list_files():
            #     print(storage.child(i.name))
            fName = filename+str(int(time.time()))+".csv"
            storage.child(fName).put(final_encoded_path)

            json_data = data.to_json()
            data=data.head(50)
            df = str(data.to_html())
            # print(data.to_json())
            return json.dumps({'success':True, 'data': df, 'ogFileName': file.filename,  'nameText': fName, 'json_data': json_data }), 200, {'ContentType':'application/json'}
    else:
        return json.dumps({'success':True, 'data': "Get Method"}), 200, {'ContentType':'application/json'}


@app.route("/")
def Home():
	return "Hello"

def process_data(path, filename):
    """ Function will take the uploaded csv and perform Cleaning and return the cleaned CSV """
    # Call Continuous data preprocessing
    # Call Categorical data preprocessing
    print("Preprocessing Started")
    data = ContinuousPreProcess(path+"\\"+filename)
    print("Done Preprocessing Continuous")
    data.to_csv(path+"\\"+filename.replace(".csv", "")+"_Continuous_Processed.csv", header=True, index=False)
    print("File saved")
    continuous_processed_path = path+"\\"+filename.replace(".csv", "")+"_Continuous_Processed.csv"
    categorical_processed_path, n = process_categorical(path+"\\"+filename.replace(".csv", "")+"_Continuous_Processed.csv", filename)
    print("Done Preprocessing Categorical")
    final_encoded_path = encodeData(categorical_processed_path, n)
    print("File Encoded") 

    return (continuous_processed_path, categorical_processed_path, final_encoded_path)


def process_categorical(path_of_csv, filename):
    """ Function to process Categorical Data """
    
    df = pd.read_csv(path_of_csv) # reading csv file
    n = len(df.index) # getting the length of the dataset
    sr = df.isnull().sum() # finding total number of nulls in each column
    sr = sr.sort_values(ascending = False) # sorting the series in descending order of total number of nulls present in a column
    df_keys = sr.keys()

    for i in range(len(df_keys)):

        if(sr.get(key = df_keys[i])==0): break
        if(not isCategorical(df[df_keys[i]], n)): continue

        l1 = df.drop([df_keys[i]], axis = 1).dropna().index.tolist() # keeps a track of all rows which do not have any null values except df_keys[i]
        l2 = df[df[df_keys[i]].isnull()].index.tolist() # keeps a track of all null values in df_keys[i]
        l3 = [index for index in l1 if index in l2]
        to_predict = df.loc[l3]
        df_pred = predict_val(df.dropna(), df_keys[i], to_predict) # predicting the values at the null places
        df[df_keys[i]].loc[l3] = df_pred
        print(df_keys[i], df_pred)

    df = df.dropna()
    df.to_csv(path_of_csv.replace("_Continuous_Processed.csv","")+"_Categorical_Processed.csv", header=True, index=False)
    return (path_of_csv.replace("_Continuous_Processed.csv","")+"_Categorical_Processed.csv", n)


def encodeData(path_of_csv, n):
    """ Funtion to encode the CSV file with strings to one hot encoded columns """

    df = pd.read_csv(path_of_csv)
    only_str = []
    to_remove = []
    n = len(df.index)
    print("====================")
    print("====================")
    print(df.columns)
    print("====================")
    print("====================")
    for i in range(len(df.columns)-1):
        if(type(df[df.columns[i]].iloc[0]) == str):
            only_str.append(df.columns[i])

    print("====================")
    print("====================")
    print(only_str)
    print("====================")
    print("====================")

    for i in only_str:
        if(not isCategorical(df[i],n)): 
            to_remove.append(only_str.pop(only_str.index(i)))

    print("----------------------------------")
    print(only_str)

    to_remove.append(df.columns[-1])

    # df = df.drop(to_remove, axis = 1)
    column_trans_final = make_column_transformer((OneHotEncoder(handle_unknown='ignore'), only_str), remainder='passthrough')
    df = column_trans_final.fit_transform(df)
    df = pd.DataFrame(df)
    print(column_trans_final.get_feature_names())
    df = df.dropna()
    df.columns = column_trans_final.get_feature_names()
    # print(df)
    df.to_csv(path_of_csv.replace("_Categorical_Processed.csv", "_Final_Encoded.csv"), index=False)

    return path_of_csv.replace("_Categorical_Processed.csv", "_Final_Encoded.csv")

'''
@app.route('/uploadBuilder', methods=['POST'])
def onUploadBuilder():
    response="No file received"
    if request.method=='POST':
        f=request.files.get('File')      
        df=pd.read_csv(f)
        problem_type=request.form['problem_type']
        filteredRows=request.form['rows'].split(",")
        filteredCols=request.form['cols'].split(",")
        outputcol=int(request.form['outputcol'])
        useremail=request.form['useremail']
        username=useremail.split("@")[0].split(".")[0]
        print(useremail.split("@")[0].split(".")[0])
        # converting boolean lists to numbers
        filteredRowsLst=[]
        filteredColsLst=[]
        for i in range(len(filteredRows)):
            if(filteredRows[i]=="true"): filteredRowsLst.append(i)
        for i in range(len(filteredCols)):
            if(filteredCols[i]=="true"): filteredColsLst.append(i)


        if(problem_type=="regression"):
            cat = df.select_dtypes(include='O').keys()
            lenc=len(cat)
            new_df = df[cat].copy()
            cat_columns=[]
            # column name and unique values in each column
            for x in new_df.columns:
                for i in range(lenc):
                    list_col=[]
                    list_col.append(x)
                    list_col.append(len(new_df[x].unique()))
                cat_columns.append(list_col)
            column_name=[]
            for i in range(lenc):
                column_name.append(cat_columns[i][0])
            #number of times value occurs
            column_number=[]
            for i in range(lenc):
                column_number.append(cat_columns[i][1])
            column_values=[]
            for i in range(lenc):
                for j in range(column_number[i]):
                    column_values=df[column_name[i]].unique()
                    for k in range(column_number[i]):
                        df[column_name[i]].replace({column_values[k]: k}, inplace=True)
        
        X=df.iloc[filteredRowsLst,filteredColsLst]
        Y=df.iloc[filteredRowsLst,outputcol]
        
        customOutput=("algo",0.0,"")
        resMsg=""
        if(problem_type=="binary" or problem_type=="multiclass"):
            customOutput=getClassificationCustomModel(X,Y)
        else:
            customOutput=getRegressionCustomModel(X,Y)
        libraryOutput=getBestModel(X,Y,problem_type)
        # uploadToFirebase(libraryOutput[2],useremail)
        if(libraryOutput[1]>customOutput[1]):
            libraryOutput[2].save(username+'.pkl')
            resMsg="Selected "+libraryOutput[0]+" algorithm with accuracy "+'%0.2f'%(libraryOutput[1]*100)+"%"
            
        else:
            resMsg="Selected "+customOutput[0]+" algorithm with accuracy "+'%0.2f'%(customOutput[1]*100)+"%"
            pickle.dump(customOutput[2], open(username+'.pkl', 'wb'))
        inputColumns=[]
        for s in X.columns:
            inputColumns.append('"'+s+'"')
        inputColumns=",".join(inputColumns)
        inputColumns="["+inputColumns+"]"
        inputColsDtypes=[]
        for s in list(map(str,list(X.dtypes))):
            inputColsDtypes.append('"'+s+'"')

        inputColsDtypes=",".join(inputColsDtypes)
        inputColsDtypes="["+inputColsDtypes+"]"
        f = open(username+".py", "w")
        f.write("""
from tkinter import filedialog
from tkinter import *
import pickle
import evalml
import pandas as pd
import numpy as np
import os
window=Tk()
input_var=StringVar()
row=Frame(window)
row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
input_label = Label(row, text = 'Enter values separated by "," \\n """+inputColumns+"""', font=('calibre',10, 'bold'),wraplength=500)
input_label.pack()
row=Frame(window)
row.pack(side = TOP, fill = X, padx = 10 , pady = 5)
input_entry = Entry(window,textvariable = input_var, font=('calibre',10,'normal'),justify="center",width=50)
input_entry.pack(fill = X,padx=10)
row=Frame(window)
row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
output_label =Label(window,text="",font=('calibre',10, 'bold'))
output_label.pack()  
def browse_file():
    global df
    import_file_path = filedialog.askopenfilename(initialdir = os.getcwd(),filetypes=[("csv files","*.csv")])
    read_file = pd.read_csv (import_file_path)
    df = pd.DataFrame(read_file) 
    getMultipleOutput()
def getOutput():
    with open('"""+username+""".pkl' , 'rb') as f:
        model = pickle.load(f)
    temp=input_var.get().split(",")
    data=[]
    input_var.set("")
    datatypes="""+inputColsDtypes+"""
    for j in range(len(datatypes)):
        if(datatypes[j]=="int64"):
            data.append(int(temp[j]))
        elif(datatypes[j]=="float64"):
            data.append(float(temp[j]))
        else:
            data.append(temp[j])
    data=[data]
    X = pd.DataFrame(data, columns ="""+inputColumns+""")
    output_label['text']=model.predict(X).iloc[0]
def getMultipleOutput():
    with open('"""+username+""".pkl' , 'rb') as f:
        model = pickle.load(f)
    X = pd.DataFrame(df, columns ="""+inputColumns+""")
    Y=model.predict(X)
    df['OUTPUT']=Y.to_series()
    print(df.head())
    writer = pd.ExcelWriter('demo.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
row=Frame(window)
row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
button_singleInput = Button(window, text ="Submit", command=getOutput)
button_singleInput.pack(padx = 5, pady = 5)
row=Frame(window)
row.pack(side = TOP, fill = X, padx = 5 , pady = 5)
button_multipleInput = Button(window, text ="Upload Exelsheet", command=browse_file)
button_multipleInput.pack(padx=5,pady=5)
window.title('Sample Usage')
window.geometry("600x400+10+20")
window.mainloop()""")
        f.close()
        msg = Message("Here's Your Machine Learning Model!",sender="prithvirajpatil2511@gmail.com",recipients=[useremail])

        with app.open_resource(username+".pkl") as fp:
            msg.attach(username+".pkl", username+"/pkl", fp.read())
        
        with app.open_resource(username+".py") as fp:
            msg.attach(username+".py", username+"/py", fp.read())
        print("Mail bhej diya hai")
        mail.send(msg)
        os.remove(username+".py")
        os.remove(username+".pkl")
        response = jsonify(message=resMsg)
    return response




def getClassificationCustomModel(X,Y):
    
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)
    sc = StandardScaler() 
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    classifier1 = SVC(kernel = 'rbf', random_state = 0) 
    classifier1.fit(X_train, y_train) 
    classifier2 = LogisticRegression(random_state = 0)
    classifier2.fit(X_train, y_train)
    classifier3 = DecisionTreeClassifier(criterion='entropy', random_state=0)
    classifier3.fit(X_train, y_train)
    classifier4 = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
    classifier4.fit(X_train, y_train)
    accuracies1 = cross_val_score(estimator = classifier1, X = X_train, y = y_train, cv = 10) 
    Mean1=accuracies1.mean() 
    accuracies2 = cross_val_score(estimator = classifier2, X = X_train, y = y_train, cv = 10) 
    Mean2=accuracies2.mean() 
    accuracies3 = cross_val_score(estimator = classifier3, X = X_train, y = y_train, cv = 10) 
    Mean3=accuracies3.mean() 
    accuracies4 = cross_val_score(estimator = classifier4, X = X_train, y = y_train, cv = 10) 
    Mean4=accuracies4.mean() 
    Final=max(Mean1,Mean2,Mean3,Mean4)
    FinalClassifier=""
    if(Final==Mean1):
        FinalClassifier=classifier1
        y_pred = classifier1.predict(X_test)
        algo="Support Vector Classification"
    elif(Final==Mean2):
        FinalClassifier=classifier2
        algo="Logistic Regression"
        y_pred = classifier2.predict(X_test)
    elif(Final==Mean3):
        FinalClassifier=classifier3
        algo="Decision Tree"
        y_pred = classifier3.predict(X_test)
    else:
        FinalClassifier=classifier4
        algo="Random Forest"
        y_pred = classifier4.predict(X_test)
    print(algo,Final)
    return(algo,Final,FinalClassifier)
    
def getRegressionCustomModel(X,Y):
    print("------------------------------------------------------")
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33, random_state=1)
    sc = StandardScaler() 
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)
    regressor1 = LinearRegression() 
    regressor1.fit(np.array(X_train), y_train)  
    regressor2 = RandomForestRegressor(random_state = 0)
    regressor2.fit(np.array(X_train), y_train) 
    regressor3 = SVR(kernel='rbf')
    regressor3.fit(np.array(X_train), y_train) 
    regressor4 = DecisionTreeRegressor(random_state = 0) 
    regressor4.fit(np.array(X_train), y_train) 

    accuracies1 = cross_val_score(estimator = regressor1, X = X_train, y = y_train, cv = 10) 
    Mean1=accuracies1.mean() 
    accuracies2 = cross_val_score(estimator = regressor2, X = X_train, y = y_train, cv = 10) 
    Mean2=accuracies2.mean() 
    accuracies3 = cross_val_score(estimator = regressor3, X = X_train, y = y_train, cv = 10) 
    Mean3=accuracies3.mean()
    accuracies4 = cross_val_score(estimator = regressor4, X = X_train, y = y_train, cv = 10) 
    Mean4=accuracies4.mean()  
    Final=max(Mean1,Mean2,Mean3,Mean4)
    FinalRegressor=""
    if(Final==Mean1):
        FinalRegressor=regressor1
        y_pred = regressor1.predict(np.array(X_test)) 
        algo="LinearRegression"
    elif(Final==Mean2):
        FinalRegressor=regressor2
        algo="Random Forest Regression"
        y_pred1 = regressor2.predict(np.array(X_test)) 
    elif(Final==Mean3):
        FinalRegressor=regressor3
        algo="Support Vector Regression"
        y_pred1 = regressor3.predict(np.array(X_test)) 
    else:
        FinalRegressor=regressor4
        algo="Decision Tree Regression"
        y_pred1 = regressor4.predict(np.array(X_test)) 
    print(algo,Final)
    return(algo,Final,FinalRegressor)


def getBestModel(X,Y,problem_type):
    X_train,X_test,y_train,y_test=evalml.preprocessing.split_data(X,Y,problem_type=problem_type)
    automl = AutoMLSearch(X_train=X, y_train=Y, problem_type=problem_type,optimize_thresholds=True)
    automl.search()
    best_pipeline=automl.best_pipeline
    if(problem_type=="regression"):
        finalScore=best_pipeline.score(X_test, y_test,  objectives=["R2"])
        print(finalScore)
        return (best_pipeline.name,finalScore["R2"],best_pipeline)
    elif(problem_type=="binary"):
        finalScore=best_pipeline.score(X_test, y_test,  objectives=["auc"])
        print(finalScore)
        return (best_pipeline.name,finalScore['AUC'],best_pipeline)
    else:
        finalScore=best_pipeline.score(X_test, y_test,objectives=["Accuracy Multiclass"])
        print(finalScore)
        return (best_pipeline.name,finalScore['Accuracy Multiclass'],best_pipeline)
    
    


# def uploadToFirebase(best_pipeline,useremail):
#     config={
#         "apiKey": "AIzaSyDg7ZaiX-TR23QbfMeHY1Ig5mPV_AQp3UI",
#         "authDomain": "automl-16092.firebaseapp.com",
#         "databaseURL": "https://automl-16092.firebaseapp.com",
#         "projectId": "automl-16092",
#         "storageBucket": "automl-16092.appspot.com",
#         "messagingSenderId": "165718849723",
#         "appId": "1:165718849723:web:37124bd74ef006ec27919e",
#         "measurementId": "G-04XQHTMDEB"
#     }
#     firebase=pyrebase.initialize_app(config)
#     storage=firebase.storage()
#     path_on_cloud="models/"+useremail+".pkl"
#     storage.child(path_on_cloud).put(best_pipeline.save(useremail+'.pkl'))
    



'''
if __name__=='__main__':
    app.run()