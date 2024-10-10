from school.Model_Owner import Model
from school.Data_Processor import DataProcessor

class Connectinator:
    def __init__(self, model_path = ''):
        # Creating model class from the model_owner file
        self.model = Model(model_path)

        # Creating data processor class
        self.data_processor = DataProcessor()

    # Process frame
    def process_frame(self, keypoints):
        self.data_processor.add_frame(keypoints)

    # Get model prediction
    def predict_model(self, keypoints):
        return self.model.query_model(keypoints)