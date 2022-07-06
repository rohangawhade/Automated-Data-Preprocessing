# from dis import dis
from zipfile import ZipFile, ZIP_DEFLATED
import os
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
import cv2
import glob
import json
import base64

# from pyLDAvis import display

def UnzipFolder(folder_path, user):
    with ZipFile(folder_path+"\\"+user, 'r') as zipObj:
        zipObj.extractall(folder_path)
        user = user.replace(".zip", "")
    return user


def ImageProcess(folder_path, user):
    folder_names = os.listdir(folder_path)
    print("Folder Names: ", folder_names)
    # Store the folder names in class_names dictionary
    class_names = {}
    for name in folder_names:
        try:
            print("LINE 23")
            print(folder_path+name)
            class_names[name] = (os.listdir(folder_path+"\\"+name))
        except:
            continue
    print("Class Names: ",class_names, user)
    # Store images in array form
    img_size = 224
    files = []
    ct = 0
    displayImages = []
    print("---!!!!!---*********----!!!----")
    for i in class_names[user]:
        print("-----------*********------------")
        print(i)
        print(folder_path+"\\"+user+"\\"+i+"\\*.*")
        images = []
        for img in glob.glob(folder_path+"\\"+user+"\\"+i+"\\*.*"):
            # print("img printing %^#@^&*#@*")
            # print(img)
            img_arr = cv2.imread(img)[...,::-1]
            # print("here")
            if ct < 5:
                data = {}
                with open(img, mode='rb') as file:
                    img = file.read()
                data["img"] = base64.encodebytes(img).decode('utf-8')
                displayImages.append(json.dumps(data))
                ct += 1
            img_arr = cv2.resize(img_arr, (img_size, img_size))

            if(img_arr.shape[2] == 3):  # if image is colored (RGB)
                img_arr_reshape = img_arr.reshape(img_arr.shape[0], -1)  # reshape it from 3D matrice to 2D matrice

            else:  # if image is grayscale
                img_arr_reshape = img_arr

            images.append(img_arr_reshape)
        images = np.array(images)
        np.save(i, images)
        files.append(i+'.npy')
    print("PRINTING IMAGES ARRAY")
    print(displayImages)
    print("PRINTING IMAGES ARRAY")
    return (files, displayImages)


def CheckZip(folder_path, user):
    if user.endswith(".zip"):
        user = UnzipFolder(folder_path, user)
        print(f'{user} unzipped')
    print(folder_path, "_________"+ user)
    class_names, displayImages = ImageProcess(folder_path, user)
    pth = user+'.zip'
    with ZipFile(user+'.zip', 'w') as zipF:
        for file in class_names:
            zipF.write(file, compress_type=ZIP_DEFLATED)
    print('Final zip file saved')
    return (pth, displayImages)


def processImage(UPLOAD_FOLDER, filename):
    folder_path = UPLOAD_FOLDER
    user = filename
    print("-----------------------------------------------")
    print(folder_path, "++++++++++", user)
    path, displayImages = CheckZip(folder_path, user)
    return (path, displayImages)
 