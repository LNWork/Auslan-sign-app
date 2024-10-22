import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv(override=True)

genai_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure()
class ResultsParser:

    def parse_model_output(self, model_output):
        """
        Parses the output from the sign language model and saves the best word 
        with the highest confidence to a JSON file.
        
        Args:
            model_output (list of tuples): Output from the model, expected as a list of (word, confidence) tuples.
        """
        if not model_output:
            # To DO: Log error here.
            return {"error": "No output from model"}

        # Find the word with the highest confidence
        best_model_phrase, best_confidence = max(model_output, key=lambda item: item[1])

        if len(best_model_phrase.split()) > 2:
            print("contacting gemini")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content("Convert these words into a correct English sentence:"+ best_model_phrase)
            response_dict = response.to_dict()
            result = response_dict["candidates"][0]["content"]["parts"][0]["text"].strip('"').replace("\n", "").replace("\"", "")
            print(result)
        else:
            result = best_model_phrase
            
        return result

    def save_as_json(self, parsed_result, output_filename="parsed_result.json"):
        """
        Save the parsed result as a JSON file.
        """
        with open(output_filename, 'w') as outfile:
            json.dump(parsed_result, outfile, indent=4)
            print(f"Saved parsed result to {output_filename}")



