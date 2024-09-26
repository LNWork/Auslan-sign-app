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

        # Prepare the result
        result = {
            "word": best_word,
            "confidence": best_confidence
        }

        # Write the result to a JSON file
        with open('parsed_result.json', 'w') as outfile:
            json.dump(result, outfile, indent=4)

        
        print(f"Best Word: {best_word}, Confidence: {best_confidence}")

# Manual testing
if __name__ == "__main__":
    # Example manual input
    model_output = [
        ["hello", 0.95],
        ["hi", 0.75],
        ["greetings", 0.60]
    ]

    # Create an instance of ResultsParser
    parser = ResultsParser()
    
    # Parse the model output and save to JSON
    parser.parse_model_output(model_output)
