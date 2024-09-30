import json
import os


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def save_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)


def combine_json_files(directory, output_file):
    combined_data = []
    frame_count = 0

    # Get all JSON files in the directory
    json_files = [f for f in os.listdir(directory) if f.endswith('.json')]

    for json_file in sorted(json_files):
        file_path = os.path.join(directory, json_file)
        data = load_json(file_path)

        for frame_data in data:
            # Update frame count
            frame_data['frame'] = frame_count
            combined_data.append(frame_data)
            frame_count += 1

    # Save the combined data into a new JSON file
    save_json(combined_data, output_file)
    print(f"Combined {len(json_files)} files into {output_file}")


# Directory containing JSON files and the output file
input_directory = 'folder'
output_file = 'scripts/combined_output.json'

combine_json_files(input_directory, output_file)
