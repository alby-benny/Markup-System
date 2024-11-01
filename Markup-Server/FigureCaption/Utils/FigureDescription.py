import pathlib
import textwrap
import google.generativeai as genai
import PIL.Image
import cv2
import numpy as np
import os

genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro-vision')

def count_files_in_folder(folder_path):
    DesTemp = []
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return -1

    file_count = 0
    # Walk through the directory tree
    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)
        for file in files:
            DesTemp.append(file)

    return file_count,DesTemp

def captioning(qno):
    fd_ans={}
    for k in range(len(qno)):
        x = "FigureDetection/Figures/QNO" + str(qno[k])
        n,FileNames = count_files_in_folder(x)
        i=0
        for j in FileNames:
            img = PIL.Image.open(x+"/"+j)
            response = model.generate_content(["Describe this image in english", img], stream=True)
            response.resolve()

            #fd_ans[str(qno[k])+"_"+j.replace('.jpg','')] = response.text
            fd_ans[str(qno[k])] = response.text
    return fd_ans