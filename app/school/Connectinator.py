from school.Model_Owner import Model
from school.InputParser import InputParser


class Connectinator:
    def __init__(self, model_path=''):
        # Creating model class from the model_owner file
        self.model = Model(model_path)

        # Creating data processor class
        self.inputProc = InputParser()

    # Process frame
    def process_frame(self, keypoints):
        self.inputProc.process_frame(keypoints)

    # TODO: LISTENER FOR RECEIVE FROM SAVE CHUNK, SEND TO MODEL

    # Get model prediction
    def predict_model(self, keypoints):
        return self.model.query_model(keypoints)

    # TODO: LISTENER FOR RECEIVE OUTPUT FROM MODEL, ADD TO LIST, SEND TO RESULTS PARSER
    # TODO: RESET LIST WHEN CAMERA FINISHED

    # TODO: RESULTS PARSER ASYNC UPDATE FRONT END TEXT FIELD
