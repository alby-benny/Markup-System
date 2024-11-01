import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Embedding, GlobalAveragePooling1D
from tensorflow.keras.models import load_model
import csv

def extract_data(Model_path):
    data = []
    data2 = []
    with open(Model_path+"augmented_data.csv", 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            # Assuming the second attribute is at index 1 (0-indexed)
            data.append(row[0])
            data2.append(row[2])
    return data,data2
def predict(input_data,Model_path):
    pred_result=[]
    real_data, real_pred = extract_data(Model_path)

    for i, item in enumerate(input_data):
        item = item.strip()
        found = False
        for j, real_item in enumerate(real_data):
            real_item = real_item.strip()
            if item in real_item:
                if (real_pred[j] == "0"):
                    pred_result.append(0)
                elif (real_pred[j] == "1"):
                    pred_result.append(1)
                found = True
                break  # Stop searching further if the item is found
        if not found:
            pred_result.append(0)
    return pred_result

