import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(override=True)

genai_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure()

class textAnimationTranslation:

    def parse_text_to_sign(self, t2s_input):

        #if isinstance(t2s_input, list) and len(t2s_input) > 0:
        #    t2s_input = t2s_input[0]

        if not t2s_input:
            # To DO: Log error here.
            return {"error": "Invalid input from user"}
        
        if len(t2s_input.split()) > 2:
            print("Contacting Gemini")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content("Convert this phrase into an Auslan english Sentence (as text) Provide only the text no other explanation:"+ t2s_input + "Use the following as an example, I am going to the park tomorrow translates to, tomorrow park me go")
            response2 = model.generate_content("Convert this phrase into a sign-language english Sentence (as text) Provide only the text no other explanation:"+ t2s_input)
            response_dict = response.to_dict()
            response2_dict = response2.to_dict()
            if response_dict["candidates"]:
                result = response_dict["candidates"][0]["content"]["parts"][0]["text"].strip().replace("\n", "").replace("\"", "")
            else:
                result = "No valid response"
            
            # Safely accessing the text from the second response
            if response2_dict["candidates"]:
                result2 = response2_dict["candidates"][0]["content"]["parts"][0]["text"].strip().replace("\n", "").replace("\"", "")
            else:
                result2 = "No valid response"
            print(result)
            print(result2)

        else:
            result = t2s_input
            result2 = 'N/A'

        return result
    
    def save_as_json(self, parsed_result, output_filename="parsed_input.json"):
        """
        Save the parsed input as a JSON file.
        """
        with open(output_filename, 'w') as outfile:
            json.dump(parsed_result, outfile, indent=4)
            print(f"Saved parsed result to {output_filename}")