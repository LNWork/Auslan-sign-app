from school.Model_Owner import Model
from school.InputParser import InputParser
import logging
from school.results_parser import ResultsParser
from school.results_parser import textAnimationTranslation


def create_logger():
    # Set up logging
    logger = logging.getLogger()  # Create a logger
    logger.setLevel(logging.INFO)  # Set the logging level

    # Create a file handler to log messages to a file
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.INFO)  # Set the file logging level

    # Create a console handler to log messages to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set the console logging level

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


class Connectinator:
    def __init__(self, model_path=''):
        # Creating logger
        self.logger = create_logger()

        # Creating model class from the model_owner file
        self.model = Model(model_path)

        # Creating data processor class
        self.inputProc = InputParser()

        # Create result parser
        self.results_parser = ResultsParser()

        # Create text ani transltior
        self.text_animation_translation = textAnimationTranslation()

        self.predictionList = []
        self.phraseFlag = False

    # Process the model output
    def format_model_output(self, output):
        processed_output = self.results_parser.parse_model_output(output)

        return processed_output

    # Return auslan grammer sentence
    def format_sign_text(self, input):
        processed_t2s_phrase = self.text_animation_translation.parse_text_to_sign(
            input)

        return processed_t2s_phrase

    # Process frame
    def process_frame(self, keypoints):
        keyPointChunk, eof = self.inputProc.process_frame(keypoints)
        if eof:
            # TODO: DECIDE WHAT TO DO WITH END OF PRHASE
            print("END OF PHRASE")
        if keyPointChunk is not None:
            return self.predict_model(keyPointChunk)

    # TODO: LISTENER FOR RECEIVE FROM SAVE CHUNK, SEND TO MODEL

    def phraseListener(self, pred):
        self.predictionList.append(pred)
        if self.phraseFlag:
            # define end of phrase
            # send to magic
            print("send to magic here")
            self.predictionList = []
            self.phraseFlag = False

    # Get model prediction

    def predict_model(self, keypoints):
        predictions = self.model.query_model(keypoints)
        self.phraseListener(predictions)

        return predictions

    # TODO: MODEL RESULTS ADDED TO LIST
    # TODO: IF END OF PHRASE, SEND TO RESULTS PARSER IN LIST
    # TODO: RESULTS PARSER UPDATE FRONT END TEXT FIELD
