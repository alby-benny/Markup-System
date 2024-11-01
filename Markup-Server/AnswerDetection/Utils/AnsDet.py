from pdf2image import convert_from_path
import matplotlib.pyplot as plt
from PIL import Image
import os
import shutil
import pytesseract

def cut_image_by_y(image, y_coordinate):
    # Check if the y-coordinate is within the image bounds
    if y_coordinate >= image.height:
        print("Y-coordinate is out of bounds.")
        return

    # Split the image into two parts based on the y-coordinate
    top_half = image.crop((800, 0, image.width, y_coordinate))
    bottom_half = image.crop((0, y_coordinate, image.width, image.height))
    #plt.imshow(top_half)
    #plt.show()
    return top_half

def copy_contents(source_dir, destination_dir):
    # Get the list of files and directories in the source directory
    contents = os.listdir(source_dir)

    # Iterate through each item in the source directory
    for item in contents:
        # Formulate the full path of the item
        source_item = os.path.join(source_dir, item)
        # Formulate the full path of the destination item
        destination_item = os.path.join(destination_dir, item)

        # Check if the item is a file
        if os.path.isfile(source_item):
            # Copy the file to the destination directory
            shutil.copy(source_item, destination_item)
        # Check if the item is a directory
        elif os.path.isdir(source_item):
            # Copy the directory to the destination directory recursively
            shutil.copytree(source_item, destination_item)

def Detect(AnsPath):
    images = convert_from_path(AnsPath)
    ls = 0
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save('AnswerDetection/Temp/hi' + str(i + 1) + '.jpg', 'JPEG')

    img = Image.open("AnswerDetection/Temp/hi1.jpg")
    crop1 = cut_image_by_y(img, 155)

    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(crop1, config=custom_config)
    source_directory = "D:\ANSWERS"
    destination_directory = "AnswerDetection/Answers/"

    copy_contents(source_directory, destination_directory)