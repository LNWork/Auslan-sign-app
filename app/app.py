from flask import Flask, request, jsonify, render_template
from results_parser import ResultsParser

from markupsafe import escape

app = Flask(__name__)

results_parser = ResultsParser()

@app.route("/")
def index():
    return render_template('keypoints.html')

@app.route('/sign_to_text')
def run_text_to_sign():
    return render_template('text_to_sign.html')

@app.route('/model_output', methods=['GET', 'POST'])
def model_output_parse():
    model_output = request.get_json()
    model_output_data = model_output['model_output']
    print("Received Model Output:", model_output)
    processed_output = results_parser.parse_model_output(model_output_data)

    return jsonify({"message": processed_output}), 200
 
@app.route('/api/keypoints', methods=['POST'])
def receive_keypoints():
    data = request.json  # Get the JSON data from the request
    # keypoints = data.get("keypoints")  # Extract keypoints from the received data
    # You can process, store, or log the keypoints here
    print("Received landmarks:", data)  # Print keypoints for demonstration

    return jsonify({"message": "Keypoints received successfully!"})
if __name__ == "__main__":
    app.run(debug=True)

