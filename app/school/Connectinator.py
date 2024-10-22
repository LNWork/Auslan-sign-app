from school.Model_Owner import Model
from school.InputParser import InputParser
from school.GrammarParser import textAnimationTranslation
from school.results_parser import ResultsParser

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
    def parse_text_to_sign(self, t2s_input):
        text_translation = textAnimationTranslation()
        t2s_parse_phrase = t2s_input['t2s_input']
        processed_t2s_phrase = text_translation.parse_text_to_sign(t2s_parse_phrase)
        return processed_t2s_phrase
    
    def parse_model_output(self, model_output):
        model_output_parsed = ResultsParser()
        model_output_data = model_output['model_output']
        processed_output = model_output_parsed.parse_model_output(model_output_data)
        return processed_output
