import json
class ResultsParser:
    def __init__(self):
        pass



    def parse_model_output(self, model_output):
        """
        Parses the output from the sign language model and saves the best word 
        with the highest confidence to a JSON file.
        
        Args:
            model_output (list of tuples): Output from the model, expected as a list of (word, confidence) tuples.
        """
        if not model_output:
            # If there is no output, you could return or log an error
            return {"error": "No output from model"}

        # Find the word with the highest confidence
        best_word, best_confidence = max(model_output, key=lambda item: item[1])

        print(f"Best Word: {best_word}, Confidence: {best_confidence}")

        # Prepare the result
        result = {
            "word": best_word,
            "confidence": best_confidence
        }

        return result

    def save_as_json(self, parsed_result, output_filename="parsed_result.json"):
        """
        Save the parsed result as a JSON file.
        """
        with open(output_filename, 'w') as outfile:
            json.dump(parsed_result, outfile, indent=4)
            print(f"Saved parsed result to {output_filename}")

def load_model_output(file_path):
        with open(file_path, 'r') as file:
             data = json.load(file)
             return data["model_output"]

# Manual testing
if __name__ == "__main__":
    # Example manual input
    # model_output = [
    #     ["hello", 0.95],
    #     ["hi", 0.75],
    #     ["greetings", 0.60]
    # ]

    # Create an instance of ResultsParser
    parser = ResultsParser()

    # Path to the model_output.json file (adjust path as needed)
    model_output_file = "src/model_output.json"
    
    # Load the model output from JSON file
    model_output = load_model_output(model_output_file)

    # Parse the results
    parsed_result = parser.parse_model_output(model_output)
    
    # Save the parsed result to a new JSON file
    parser.save_as_json(parsed_result)