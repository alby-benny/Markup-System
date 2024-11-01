from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from IQA_Files.utils import IQA
import pandas as pd
import tabula
import csv
import os
import shutil
from AnswerDetection.Utils import AnsDet
from FigureDetection.Utils import Extraction
from FigureCaption.Utils import FigureDescription
from FigureCaption.Utils import FigureDescritionPdf
from FigureComparision.Utils import FigureSimilarity
from HWR.Utils import Hwr
from MarkDistribution.Utils import AssignMark
import json


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["POST"])
QnoList=[]
@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...)):
    # Check if a file was sent in the request
    if not file:
        return {"error": "No file provided"}
    removeOld("AnswerDetection/Answers")
    removeOld("FigureDetection/Figures")
    # Save the file to a temporary location
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    extract_text_from_pdf(file_path)
    IQA.figureRequriment()

    df = pd.read_csv("IQA_Files/Result/modified.csv")
    json_data = df.to_json(orient="records")
    message = {"Message": "PDF processed successfully"}
    response_data = {**message, "Data": json_data}
    return response_data

    #return {"Message": "PDF processed successfully"}

@app.post("/process-answer")
async def process_pdf(file: UploadFile = File(...)):
    # Check if a file was sent in the request
    if not file:
        return {"error": "No file provided"}

    # Save the file to a temporary location
    file_path = os.path.join("uploads", file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    AnsDet.Detect(file_path)
    HwrFinal,FinalMark=FD("AnswerDetection/Answers")
    Answer = json.dumps(HwrFinal)
    Mark = json.dumps(FinalMark)
    message = {"Message": "Answer processed successfully"}
    response_data = {**message,"Answer": Answer,"Mark": Mark}
    return response_data
def removeOld(folder_path):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return -1
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            shutil.rmtree(folder_path+"/"+dir)

def FD(folder_path):
    # Check if the folder exists
    QnoList = []
    FigureTemp=[]
    fd_pdf = {}
    hwrResult_fig = {}
    hwr_norm = []
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return -1
    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            FigureTemp.append(str(dir).replace('QNO',''))
    with open('IQA_Files/Result/modified.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Requirement'] == '1' and row['QNO'] in FigureTemp:
                Extraction.extraction(row['QNO'])
                QnoList.append(row['QNO'])
                fd_pdf[row['QNO']]= FigureDescritionPdf.captioning_pdf(row['QNO'],row['Questions'])
            elif row['QNO'] in FigureTemp:
                hwr_norm.append(row['QNO'])
    fd_ans = FigureDescription.captioning(QnoList)
    fd_sim = FigureSimilarity.similarity(fd_pdf, fd_ans)
    hwrResult = Hwr.recog(hwr_norm, "AnswerDetection/Answers/QNO")
    if (len(QnoList) > 0):
        hwrResult_fig = Hwr.recog(QnoList, "AnswerDetection/AnswerWithoutFigure/QNO")
    hwrFinal = {**hwrResult, **hwrResult_fig}
    FinalMark=AssignMark.getMark(hwrFinal, fd_sim, FigureTemp, fd_ans)
    return hwrFinal,FinalMark

def extract_text_from_pdf(file_path):

    tabula.convert_into(file_path, "output.csv", output_format="csv", pages="all")
    input_filename = 'output.csv'
    output_filename = 'processed_output.csv'
    # Process the CSV file
    process_csv(input_filename, output_filename)
    print("Processing complete. Check the file:", output_filename)


def process_csv(input_file, output_file):
    with open(input_file, 'r') as file_in, open(output_file, 'w', newline='') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)
        Title=["QNO","Questions","Mark","Taxonomy","Outcome"]
        writer.writerow(Title)
        previous_row = None
        for row in reader:
            if previous_row is not None and row[0] == '':
                # Join the 2nd attribute of previous and current record if the 1st attribute of the current record is null
                previous_row[1] += " "+row[1]
            else:
                # Write the previous row if it exists and is not null
                if previous_row is not None:
                    writer.writerow(previous_row)
                # Update previous row with current row
                previous_row = row

        # Write the last row if it's not null
        if previous_row is not None and previous_row[0] != '':
            writer.writerow(previous_row)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)