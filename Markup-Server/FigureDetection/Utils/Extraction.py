from ultralytics import YOLO
import cv2
import numpy as np
import os
import shutil
import matplotlib.pyplot as plt
# Load a model
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


def extraction(qno):
    x="AnswerDetection/Answers/QNO"+str(qno)
    n = count_files_in_folder(x)
    model = YOLO("FigureDetection/Utils/best.pt")
    i = 0
    for j in range(1,n+1):
        image = cv2.imread(x+"/"+str(j)+".jpg")
        results = model.predict(source=x+"/"+str(j)+".jpg")
        output_dir = "FigureDetection/Figures/QNO"+str(qno)  # Directory to save extracted images
        os.makedirs(output_dir, exist_ok=True)  # Create directory if it doesn't exist
        FigureFlag=0
        for r in results:

            boxes = r.boxes
            for box in boxes:
                FigureFlag = 1
                b = box.xyxy[0]
                coo_1 = int(b[0])
                coo_2 = int(b[1])
                coo_3 = int(b[2])
                coo_4 = int(b[3])
                copy = image[coo_2:coo_4, coo_1:coo_3]
                new_copy_below=image[coo_4:,:]
                _, new_buffer = cv2.imencode('.jpg', new_copy_below)
                destination_directory = f"AnswerDetection/AnswerWithoutFigure/QNO{qno}/"
                os.makedirs(destination_directory, exist_ok=True)
                _, buffer = cv2.imencode('.jpg', copy)  # Encode image as JPEG
                file_path = os.path.join(output_dir, f"{i+1}.jpg")
                with open(file_path, 'wb') as f:
                    f.write(buffer)  # Write encoded image data to file
                new_file_path = os.path.join(destination_directory, f"{j}.jpg")
                with open(new_file_path, 'wb') as f:
                    f.write(new_buffer)
            i += 1
            if(FigureFlag==0):
                source_file = f"AnswerDetection/Answers/QNO{qno}/{j}.jpg"
                destination_directory = f"AnswerDetection/AnswerWithoutFigure/QNO{qno}/"
                os.makedirs(destination_directory, exist_ok=True)
                shutil.copy(source_file, destination_directory)


