from zipfile import ZipFile, ZIP_DEFLATED
import os
import numpy as np
import cv2
import glob
import json
import base64


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
        except:  # noqa: E722
            continue

    print("Class Names: ", class_names, user)

    # Store images in array form
    img_size = 224
    files = []
    ct = 0
    displayImages = []
    for i in class_names[user]:
        images = []
        for img in glob.glob(folder_path+"\\"+user+"\\"+i+"\\*.*"):
            img_arr = cv2.imread(img)[..., ::-1]
            if ct < 5:
                data = {}
                with open(img, mode='rb') as file:
                    img = file.read()
                data["img"] = base64.encodebytes(img).decode('utf-8')
                displayImages.append(json.dumps(data))
                ct += 1
            img_arr = cv2.resize(img_arr, (img_size, img_size))

            # if image is colored (RGB)
            if(img_arr.shape[2] == 3):
                # reshape it from 3D matrice to 2D matrice
                img_arr_reshape = img_arr.reshape(img_arr.shape[0], -1)
            else:  # if image is grayscale
                img_arr_reshape = img_arr

            images.append(img_arr_reshape)
        images = np.array(images)
        np.save(i, images)
        files.append(i+'.npy')
    return (files, displayImages)


def CheckZip(folder_path, user):
    if user.endswith(".zip"):
        user = UnzipFolder(folder_path, user)
    class_names, displayImages = ImageProcess(folder_path, user)
    pth = user+'.zip'
    with ZipFile(user+'.zip', 'w') as zipF:
        for file in class_names:
            zipF.write(file, compress_type=ZIP_DEFLATED)
    return (pth, displayImages)


def processImage(UPLOAD_FOLDER, filename):
    folder_path = UPLOAD_FOLDER
    user = filename
    path, displayImages = CheckZip(folder_path, user)
    return (path, displayImages)
