from school.Model_Owner import Model
from school.InputParser import InputParser
import logging
from school.results_parser import ResultsParser
from school.GrammarParser import textAnimationTranslation
import asyncio
from time import time
import json

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
        # Setting up the results list
        self.full_phrase = AsyncResultsList(self)
        self.end_phrase_flag = False
        self.front_end_translation_variable = ''

        # Creating logger
        self.logger = create_logger()

        # Creating model class from the model_owner file
        #self.model = Model(model_path)

        # Creating data processor class
        self.inputProc = InputParser()

        # Create result parser
        self.results_parser = ResultsParser()

        # Create text ani transltior
        self.text_animation_translation = textAnimationTranslation()

        self.predictionList = []
        self.phraseFlag = False

    # Process the model output
    async def format_model_output(self, output):
        processed_output = self.results_parser.parse_model_output(output)

        # Update log file
        self.logger.info('Model Output Processed Successfully! Message: %s', processed_output)  

        # Pass this then to a varable being used for the react front end.
        self.front_end_translation_variable = processed_output

        print("DONEEE")

        with open('model_output.txt', 'a+') as f:
            f.write(f"Time: {str(time())}, Phrase: {self.front_end_translation_variable}")

    # Return auslan grammer sentence
    def format_sign_text(self, input):
        processed_t2s_phrase = self.text_animation_translation.parse_text_to_sign(input)

        # Update log file
        self.logger.info('Text To Sign Processed Successfully! Message: %s', processed_t2s_phrase)  

        return processed_t2s_phrase

    # Process frame
    async def process_frame(self, keypoints):
        full_chunk, self.end_phrase_flag = self.inputProc.process_frame(keypoints)
        if self.end_phrase_flag == True:

            print(f"ITS TRUEEE {self.end_phrase_flag}")

        if full_chunk is not None:
            print("AAAAAAAAa SENT TO THE MODEL")
            # async predict the work and then add it to the self.full_phrase

            predicted_result = await self.predict_model(full_chunk)

            with open('ball.txt', 'a+') as f:
                f.write(f"time: {str(time())}, predict:")
                f.write(json.dumps(str(predicted_result)))
                f.write("\n\n")
            self.full_phrase.append(predicted_result)

        
    # TODO: LISTENER FOR RECEIVE FROM SAVE CHUNK, SEND TO MODEL

    # Get model prediction
    async def predict_model(self, keypoints):
        print("SENT TO PREDICT")
        return await self.model.query_model(keypoints)

    # TODO: LISTENER FOR RECEIVE OUTPUT FROM MODEL, ADD TO LIST, SEND TO RESULTS PARSER

# Custom list class so that it can access run async and check when stuff is added
class AsyncResultsList(list):
    def __init__(self, connectinator_instance: Connectinator, *args):
        super().__init__(*args)
        self.connectinator = connectinator_instance
        self.saved_results = None


    def append(self, item):
        self.connectinator.logger.info(f"Word added with shape {item['model_output']}")
        super().append(item) 
        
        if self.connectinator.end_phrase_flag == True:
            print("AHAHHAHAHAHAHAHHAHA ")
            asyncio.create_task(self.parse_results())
    
    # async call the connectinator.format_model_output on this list
    async def parse_results(self):
        # Reset list result 
        self.saved_results = list(self)
        self.clear()

        # Reset the flag
        self.connectinator.end_phrase_flag = False

        self.connectinator.logger.info("Parsing results asynchronously...")
        print("FORMATTING RESULTS")
        await self.connectinator.format_model_output(self.saved_results) # change to pass saves results
        
