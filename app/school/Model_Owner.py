# Import torch for model
import pandas as pd
from tensorflow.keras.models import *
import json
import numpy as np

class Model:
    def __init__(self, model_path):
        # Setting base variables
        self.model_path = model_path

        # Just remember that indexed are strings
        self.outputs = json.load(open("word_index.txt"))

        # Create model here
        self.model = load_model(filepath=model_path)

    def query_model(self, keypoints):
        # Format keypoints so it fits the model
        formatted_keypoints = self.__format_input_keypoints(keypoints)

        # Query the model
        result = self.__get_model_result(formatted_keypoints)

        # Parse results so it fits the formate needed
        final_result = self.__format_model_results(result)

        return final_result
    
    ############################# Private helper functions needed for query model #############################
    def __format_input_keypoints(self, keypoints):
        #! PLEASE GIVE SHAPE WITH (number_of_frames, number_of_keypoints, 1, features)

        # probs just padd the dataframe so it fits the inputs
        keypoints = np.expand_dims(keypoints, axis=0)  # Add a batch dimension

        return keypoints

    def __get_model_result(self, keypoints):
        # just query the model
        return self.model.predict(keypoints)[0]

    def __format_model_results(self, result):
        # Loop through resuklts and append the correct class to the probability

        fomated_results = {"model_output": []}
        for i in range(len(result)):
            #! REMOVE LATER BUT HERE CAUSE OF THE MISMATCH INDEX
            if i > 606:
                continue
            
            # Adding the results
            str_index = str(i)
            fomated_results['model_output'].append([self.outputs[str_index], result[i]])
        

        return fomated_results
    ############################# Private helper functions needed for query model #############################
