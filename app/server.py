from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from school.Connectinator import Connectinator
import logging
from markupsafe import escape

import numpy as np

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

model_path = 'loaded_bananamode_AAAAAAAAAAAAAAAAAAAAAAAAaa.keras'

# MAIN CLASS WHICH CONNECTS TO ALL THE BACK END STUFF
connectinator = Connectinator(model_path)

@app.route("/")
def index():
    return render_template('keypoints.html')

@app.route("/cam_model_test")
def model_test():
    print()
    return render_template('index.html')

@app.route('/sign_to_text')
def run_text_to_sign():
    return render_template('text_to_sign.html')
 
@app.route('/api/keypoints', methods=['POST'])
def receive_keypoints():
    data = request.json  # Get the JSON data from the request

    # You can process, store, or log the keypoints here
    print("Received landmarks:", data)  # Print keypoints for demonstration

    # Sending data to the connectinator
    connectinator.process_frame(data)

    return jsonify({"message": "Keypoints received successfully!"})

@app.route('/model_output', methods=['GET', 'POST'])
def model_output_parse():
    try:
        # why are wer getting model out put from post?
        model_output = request.get_json()
        logging.info('Received request on /model_output: %s', model_output)  # Updated log message

        processed_output = connectinator.format_model_output(model_output['model_output'])
    
        logging.info('Model Output Processed Successfully! Message: %s', processed_output)  # Updated log message
        return jsonify({"message": processed_output}), 200

    except Exception as e:
        logging.error(f'Error processing request: {e}')
        return jsonify({"error": "Internal Server Error. Check JSON Format"}), 500
    
@app.route('/t2s', methods=['POST'])
def t2s_parse():
    try:
        t2s_input = request.get_json()
        logging.info('Received request on /t2s: %s', t2s_input)

        processed_t2s_phrase = connectinator.format_sign_text(t2s_input['t2s_input'])
        
        logging.info('Text To Sign Processed Successfully! Message: %s', processed_t2s_phrase)  # Updated log message
        return jsonify({"message": processed_t2s_phrase}), 200
    except Exception as e:
        logging.error(f'Error processing request: {e}')
        return jsonify({"error": "Internal Server Error. Check JSON Format"}), 500 

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8001, debug=True)