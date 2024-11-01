from importlib.resources import path
import os,io
from google.cloud import vision
import pandas as pd
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='HWR/Utils/GVA.json'
client=vision.ImageAnnotatorClient()

hwrResult={}
def count_files_in_folder(folder_path):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return -1

    file_count = 0
    # Walk through the directory tree
    for root, dirs, files in os.walk(folder_path):
        file_count += len(files)

    return file_count

def recog(qno,answerPath):
    hwrResult = {}
    for i in qno:
        #x = "AnswerDetection/Answers/QNO" + str(i)
        x = answerPath + str(i)
        n = count_files_in_folder(x)
        if(n!=-1):
            para = ''
            for j in range(1,n+1):

                image_path=x+"/"+str(j)+".jpg"
                with io.open(image_path,'rb') as image_file:
                    content=image_file.read()
                image=vision.Image(content=content)
                response = client.document_text_detection(image=image)

                for page in response.full_text_annotation.pages:
                  for block in page.blocks:
                    for paragraph in block.paragraphs:
                        for word in paragraph.words:
                            word_text = "".join([symbol.text for symbol in word.symbols])
                            para=para+word_text+" "
                        para=para+"\n"

            hwrResult["QNO"+str(i)]=para
    return hwrResult