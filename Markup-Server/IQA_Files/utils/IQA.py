import tensorflow as tf
from IQA_Files.utils import Model
import csv
import pandas as pd

Model_path="IQA_Files/"
def extract_data_from_csv(csv_file_path):
    data = []
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            # Assuming the second attribute is at index 1 (0-indexed)
            data.append(row[1])
    return data


def write_to_csv(file_path,image_predictions):
    original_data = pd.read_csv(file_path)
    first_three_columns = original_data.iloc[:, :3]
    first_three_columns["Requirement"] = image_predictions
    first_three_columns.to_csv("IQA_Files/Result/modified.csv", index=False)

def figureRequriment():
    csv_file_path = 'processed_output.csv'
    input_data = extract_data_from_csv(csv_file_path)

    tokenizer = tf.keras.preprocessing.text.Tokenizer()
    tokenizer.fit_on_texts(input_data)
    input_data_tokenizer = tokenizer.texts_to_sequences(input_data)
    max_sequence_length = 22
    Input_data_padded = tf.keras.preprocessing.sequence.pad_sequences(input_data_tokenizer, maxlen=max_sequence_length)
    image_predictions = Model.predict(input_data, Model_path)  # Convert probabilities to binary predictions
    file_path="processed_output.csv"
    write_to_csv(file_path,image_predictions)


