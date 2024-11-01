import pathlib
import textwrap
import google.generativeai as genai
import PIL.Image
import cv2
import numpy as np
import os

genai.configure(api_key='')
model = genai.GenerativeModel('gemini-pro-vision')

def captioning_pdf(qno,question):
    fd_pdf=''
    content = {
        "big data architecture": "BDA Architecture",
        "map reduce programming model": "Map Reduce Pipeline",
        "mapreduce model": "Map Reduce",
        "hbase": "HBase",
        "life cycle of big data analytics": "BDA Lifecycle",
        "big data platforms": "Big Data platforms",
        "big data analytics life cycle": "BDA Lifecycle",
        "hive": "Hive",
        "mapreduce execution pipeline": "Map Reduce",
        "yarn": "YARN",
        "map reduce scheduling model": "Map Reduce Pipeline",
        "pig": "Pig",
        "hdfs":"HDFS Architecture"
    }
    keys=list(content.keys())
    x = "FigureCaption/FromPDF/"

    for i in keys:
        if i in question.lower():
            img=content[i]
            img = PIL.Image.open(x+img+".jpg")
            response = model.generate_content(["Describe this image in english", img], stream=True)
            response.resolve()
            fd_pdf = response.text


    return fd_pdf