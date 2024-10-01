from flask import Flask, request, jsonify, render_template

from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('keypoints.html')
 
@app.route('/api/keypoints', methods=['POST'])
def receive_keypoints():
    data = request.json  # Get the JSON data from the request
    keypoints = data.get("poseLandmarks")  # Extract keypoints from the received data

    # You can process, store, or log the keypoints here
    print("Received landmarks:", keypoints)  # Print keypoints for demonstration

    # Respond with a success message
    return jsonify({"message": "Landmarks received successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
