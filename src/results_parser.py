import json

class ResultsParser:
    def __init__(self):
        pass

    def parse_model_output(self, model_output):
        """
        Parses the output from the sign language model and selects the word with the highest confidence.
        
        Args:
            model_output (list of tuples): Output from the model, expected as a list of (word, confidence) tuples.
        
        Returns:
            json: Parsed result in JSON format.
        """
        if not model_output:
            return json.dumps({"error": "No output from model"})

        # Assuming the model output is a list of (word, confidence) tuples
        # Example: [("hello", 0.95), ("hi", 0.75), ("greetings", 0.60)]
        
        # Find the word with the highest confidence
        best_word, best_confidence = max(model_output, key=lambda item: item[1])

        # Format the output as JSON
        result = {
            "word": best_word,
            "confidence": best_confidence
        }
        
        return json.dumps(result)

# Example of how this would work with Flask
from flask import Flask, jsonify, request

app = Flask(__name__)
parser = ResultsParser()

@app.route('/parse', methods=['POST'])
def parse():
    # Get the model output from the POST request
    model_output = request.json.get('model_output')

    # Pass the model output to the results parser
    parsed_result = parser.parse_model_output(model_output)
    
    # Return the parsed result as JSON
    return jsonify(json.loads(parsed_result))

if __name__ == "__main__":
    app.run(debug=True)
