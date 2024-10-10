from flask import Flask, render_template, request, jsonify
from school.Connectinator import Connectinator
import numpy as np

app = Flask(__name__)

model_path = 'frienddidit_cam1_200_extra.keras'

# MAIN CLASS WHICH CONNECTS TO ALL THE BACK END STUFF
connectinator = Connectinator(model_path)

@app.route("/")
def index():

    # testing the model call part
    loaded_data = np.load('exported_data.npy')
    model_result = connectinator.predict_model(loaded_data)
    print(model_result) 

    return render_template('index.html')

@app.route('/sign_to_text')
def run_text_to_sign():
    return render_template('text_to_sign.html')
 
@app.route('/api/keypoints', methods=['POST'])
def receive_keypoints():
    data = request.json  # Get the JSON data from the request

    # You can process, store, or log the keypoints here
    print("Received landmarks:", data)  # Print keypoints for demonstration

    # Sending data to the conntinator
    connectinator.process_frame(data)

    return jsonify({"message": "Keypoints received successfully!"})