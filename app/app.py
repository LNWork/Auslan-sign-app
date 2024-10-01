from flask import Flask, request, jsonify
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def index():
    return 'Index page'
 
@app.route('/api/keypoints', methods=['POST'])
def recieve_landmarks():
    data = request.json # Get the JSON data from request
    # Save keypoints
    # print("Recieved landmarks:", data) # to demo

    #Respond with a success message
    return jsonify({"message": "gotten keypoints"})


if __name__ == "__main__":
    app.run(debug=True)
