from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.utils import to_categorical
from matplotlib import pyplot as plt
import torch
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import *
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
import glob
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from tensorflow.keras.preprocessing.sequence import pad_sequences


# Path to the folder containing the JSON files
# Load the DataFrames outside of the function
isosignsDF = pd.read_excel(
    'notebooks/datasignlist.xlsx', sheet_name='IsoSigns', usecols="B:D")
singlewordDF = pd.read_excel(
    'notebooks/datasignlist.xlsx', sheet_name='SingleWord', usecols="B:D")


def normalize_keypoints(data):
    normalized_data = []

    count = 0
    for sequence in data:
        if count % 500 == 0:
            print(count)
        count += 1
        if sequence.size == 0:
            # Handle empty sequences if necessary
            normalized_data.append(sequence)  # Or use np.zeros if you prefer
            continue

        coords = sequence[..., :3]  # Extract x, y, z coordinates
        # Min values across frames
        min_vals = np.min(coords, axis=(0, 1), keepdims=True)
        # Max values across frames
        max_vals = np.max(coords, axis=(0, 1), keepdims=True)

        # Normalize the coordinates
        normalized_coords = (coords - min_vals) / (max_vals - min_vals + 1e-8)

        # Create a new array for the normalized sequence
        normalized_sequence = sequence.copy()
        # Replace x, y, z with normalized values
        normalized_sequence[..., :3] = normalized_coords
        normalized_data.append(normalized_sequence)

    return normalized_data


def get_gloss_label(file_name, isosignsDF, singlewordDF):
    # Check if the file name starts with a digit to determine which DataFrame to use
    file_name = file_name.split("/")[-1]
    if 'video_64_147_1' in file_name or 'video_64_147_1_signer_keypoints' in file_name:

    if file_name[0].isdigit():
        # Extract Video_ID from the filename
        video_id = file_name.split('_')[0]
        # Retrieve the row from the isosigns DataFrame based on Video_ID
        gloss_row = isosignsDF.loc[isosignsDF['Video_ID'] == int(video_id)]
    else:
        # Extract Video_Clip_Name from the filename
        video_clip_name = '_'.join(file_name.split('_')[:3])
        # Retrieve the row from the singleword DataFrame based on Video_Clip_Name
        gloss_row = singlewordDF.loc[singlewordDF['Video_Clip_Name']
                                     == video_clip_name]

    # Check if a match was found and return the Gloss value
    if not gloss_row.empty:
        # Note the capitalization of 'Gloss'
        return gloss_row['Gloss'].values[0]
    else:
        return None


def process_file(file):
    # print(f"Processing {file}")
    largestFrames = 0
    xData = []
    yData = []

    with open(file, 'r') as f:
        d = f.read()
        vidData = json.loads(d)

        data = []
        for frame in vidData:
            if 'data' not in frame.keys():
                continue

            fData = pd.DataFrame(frame['data'])
            data.append(fData)

        if len(data) == 0:
            return None, None, largestFrames

        combinedDF = pd.concat(data, ignore_index=True)
        reshapedData = combinedDF.values.reshape((len(data), 75, 4))
        largestFrames = max(largestFrames, len(data))

        word = get_gloss_label(file, isosignsDF, singlewordDF)

        # Handle missing gloss
        if word is None:
            print(f"Warning: No gloss label found for {file}")
            return None, None, largestFrames

        xData.append(reshapedData)
        yData.append(word)

    return xData, yData, largestFrames


if __name__ == '__main__':

    # files = glob.glob('notebooks/json_keypoints/*')
    # count = 0

    # xData = []
    # yData = []
    # largestFrames = 0

    # start = time.time()
    # count = 0
    # print("Number of files:", len(files))
    # # Create a ProcessPoolExecutor for parallel processing
    # with ProcessPoolExecutor(max_workers=8) as executor:
    #     # Use a list comprehension to submit the processing of each file
    #     futures = {executor.submit(
    #         process_file, file_name): file_name for file_name in files}

    #     for future in futures:
    #         reshaped_data, label, maxFrames = future.result()
    #         if reshaped_data is not None and label is not None:
    #             # Extend instead of append to flatten the structure
    #             xData.extend(reshaped_data)
    #             yData.append(label)
    #             largestFrames = max(largestFrames, maxFrames)

    #         if count % 500 == 0:
    #             print(count)
    #             # print(time.time()-start)
    #         count += 1

    # xData = np.array(xData, dtype=object)
    # yData = np.array(yData, dtype=object)

    # # x_train, x_test, y_train, y_test = train_test_split(
    # #     xData, yData, test_size=0.2, stratify=yData, random_state=42)

    # # print("Train samples:", len(x_train), "Test samples:", len(x_test))
    # print("Largest frames:", largestFrames)
    # print("Time taken:", time.time() - start)

    # np.savez_compressed('processed_data.npz', xData=xData, yData=yData)
    # max_length = 145
    # data = np.load('processed_data.npz', allow_pickle=True)

    # print(len(data['xData']))
    # xData = data['xData']
    # yData = data['yData']
    # print(xData.shape, yData.shape)
    # print(xData[0].shape)
    # print(yData[1])
    # print(yData[2222])
    # print(f"Unique labels in yData: {np.unique(yData)}")
    # print(f"Number of unique labels: {len(np.unique(yData))}")
    # # xData_normalized = normalize_keypoints(xData)

    # # Convert each element of yData to a hashable type (e.g., string)
    # yData_str = [str(label) if isinstance(label, np.ndarray)
    #              else label for label in yData]

    # print(len(yData_str))

    # # Get unique classes
    # # Ensure the labels are hashable
    # unique_classes = sorted(list(set(yData_str)))
    # print(unique_classes)

    # # Create a mapping from label to class index
    # label_to_class_index = {label: idx for idx,
    #                         label in enumerate(unique_classes)}
    # print(len(label_to_class_index))

    # # Map yData to class indices
    # y_mapped = [label_to_class_index[label] for label in yData_str]
    # print(f"Number of unique classes: {len(np.unique(y_mapped))}")

    # with open('label_to_class_index.json', 'w') as f:
    #     json.dump(label_to_class_index, f)

    # # xData_padded = pad_sequences(
    # #     xData_normalized, maxlen=max_length, dtype='float32', padding='post', truncating='post')

    # # print(f"Number of unique classes: {len(unique_classes)}")
    data = np.load('normalized_data.npz', allow_pickle=True)
    xData_padded = data['xData_padded']
    # xData_padded = xData_padded.reshape(
    #     (xData_padded.shape[0], xData_padded.shape[1], xData_padded.shape[2], 4, 1))
    y_mapped = data['y_mapped']

    np.savez_compressed('normalized_data.npz',
                        xData_padded=xData_padded, y_mapped=y_mapped)

    # Remove every second entry (keep only even indexed entries)
    # This keeps entries at indices 0, 2, 4, ...
    xData_reduced = xData_padded[::4]
    y_mapped_reduced = y_mapped[::4]   # Same for labels

    # Save the reduced dataset
    np.savez_compressed('reduced_normalized_data4.npz',
                        xData=xData_reduced, yData=y_mapped_reduced)
