import numpy as np
import json
import os
import pandas as pd

# Class used to store the frame data

# Parameters (adjust for real-time speed and accuracy)
THRESHOLD = 0.05
VISIBILITY_THRESHOLD = 0.7
VISIBILITY_COUNT = 0.7
WINDOW_SIZE = 30
MAX_CHUNK_LENGTH = 145  # Maximum length of a chunk in frames
HANDS_DOWN_THRESHOLD = 0.2
HANDS_DOWN_TIME = 30


class InputParser:
    def __init__(self, threshold=THRESHOLD, window_size=WINDOW_SIZE, buffer_size=5):
        self.threshold = threshold
        self.window_size = window_size
        self.buffer_size = buffer_size
        self.pause_count = 0
        self.previous_keypoints = None
        self.word_boundaries = []
        self.current_chunk = []
        self.chunks = []
        self.buffer = []
        self.chunk_counter = 0
        self.handsDownCounter = 0
        self.endOfPhrase = False

    def normalize_keypoints(self, data):
        """Normalize the keypoints data."""
        data = np.array(data)  # Convert to NumPy array
        coords = data[..., :3]  # Extract x, y, z coordinates
        min_vals = np.min(coords, axis=0, keepdims=True)
        max_vals = np.max(coords, axis=0, keepdims=True)

        # Normalize the coordinates
        normalized_coords = (coords - min_vals) / (max_vals - min_vals + 1e-8)

        normalized_data = data.copy()
        # Replace with normalized x, y, z
        normalized_data[..., :3] = normalized_coords

        return normalized_data

    def extract_keypoints(self, landmarks):
        """Extract the keypoints (x, y, z, visibility) from the landmarks."""
        try:
            return np.array([[landmark['x'], landmark['y'], landmark['z'], landmark['visibility']] for landmark in landmarks])
        except KeyError as e:
            print(f"Missing key in landmark: {e}")
            return np.empty((0, 4))

    def pad_chunk(self, chunk, max_length=MAX_CHUNK_LENGTH):
        """Pads the chunk with the last frame to reach the max length of frames."""
        chunk_length = len(chunk)  # Get the length of the chunk (a list)
        if chunk_length < max_length:
            last_frame = chunk[-1]  # Replicate the last frame
            padding_needed = max_length - chunk_length
            chunk.extend([last_frame] * padding_needed)  # Add padding
        return chunk

    def combine_keypoints(self, frame):
        """Combine pose, left hand, and right hand keypoints into a single array."""
        # combined = np.concatenate((frame['keypoints']), axis=0)
        full_data = []
        for index, keypoints in enumerate(frame):
            if keypoints != None:
                full_data += keypoints
                continue
            
            pose_number = 33 if index == 0 else 21

            match index:
                case 0:
                    full_data += [{'x': 0, 'y': 0, 'z': 0, 'visibility': 0} for _ in range(pose_number)]
                case 1 | 2:
                    full_data += [{'x': 0, 'y': 0, 'z': 0, 'visibility': 0} for _ in range(pose_number)]
                case _:
                    print("if goes here u have stuffed up")
            

        #combined = self.extract_keypoints(full_data)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(full_data)

        extracted_data = self.extract_keypoints(full_data)
        # Normalize combined keypoints
        return self.normalize_keypoints(extracted_data)

    def calculate_velocity(self, keypoints_current, keypoints_previous):
        """Calculate the velocity of keypoints between two frames."""
        velocities = np.linalg.norm(
            keypoints_current[:, :3] - keypoints_previous[:, :3], axis=1)
        return np.mean(velocities)  # Return average velocity of all keypoints

    def process_frame(self, frame):
        """Process a single frame of keypoint data in real-time."""
        keypoints_current = self.combine_keypoints(frame['keypoints'])

        handsDown = self.handsDown(
            keypoints_current[33:53], keypoints_current[54:74])
        if handsDown:
            self.handsDownCounter += 1
            print("HANDS DOWN for ", handsDownCounter)
            if self.handsDownCounter >= HANDS_DOWN_TIME:
                print("HANDS DOWN FOR TOO LONG")
                print("END OF PHRASE")
                self.endPhrase()
        else:
            handsDownCounter = 0

            # Store combined and normalized keypoints in 'data'
        frame['data'] = keypoints_current.tolist()

        if self.previous_keypoints is not None:
            velocity = self.calculate_velocity(
                keypoints_current, self.previous_keypoints)

            if velocity < self.threshold and not self.visibility_check(keypoints_current):
                self.pause_count += 1
            else:
                self.pause_count = 0

            # Check if we detect a potential boundary or chunk size exceeds limit
            if self.pause_count >= self.window_size or len(self.current_chunk) >= MAX_CHUNK_LENGTH:
                chunk_result = self.save_chunk(self.current_chunk)
                self.current_chunk = []  # Start a new chunk
                self.pause_count = 0  # Reset pause counter
                self.buffer = []  # Clear buffer
            else:
                self.buffer = []

        # Add the current frame to the chunk
        self.current_chunk.append(frame)

        # Update the previous frame's keypoints
        self.previous_keypoints = keypoints_current

        return chunk_result, self.endOfPhrase

    def save_chunk(self, chunk):
        """Save the current chunk to a JSON file in the specified format, padding it to 145 frames."""
        # os.makedirs('outputChunks',
        #             exist_ok=True)  # Ensure the output directory exists
        # filename = f"outputChunks/chunk_{self.chunk_counter}.json"

        # Pad the chunk to 145 frames if necessary
        padded_chunk = self.pad_chunk(chunk)

        # Prepare the formatted data
        chunk_data = []
        for i, frame in enumerate(padded_chunk):
            chunk_data.append({
                # Reset the frame number to start from 0 for each chunk
                "frame": i,
                # The concatenated pose, left_hand, and right_hand keypoints
                "data": frame['data']
            })

        # TODO: SEND TO CONNECTINATOR

        return chunk_data, self.endOfPhrase
        # Save to the JSON file
        # with open(filename, 'w') as f:
        #     json.dump(chunk_data, f, indent=4)

        # print(
        #     f"Chunk saved to {filename} with {len(chunk_data)} frames (padded if needed).")
        # self.chunk_counter += 1

    def visibility_check(self, keypoints):
        """Check if the visibility of keypoints is above a threshold."""
        visible_keypoints_count = (
            keypoints[..., 3] >= VISIBILITY_THRESHOLD).sum()
        total_keypoints = len(keypoints[..., 3])
        return visible_keypoints_count >= total_keypoints * VISIBILITY_COUNT

    def endPhrase(self):
        """End the current phrase and save the chunks to a file."""
        self.endOfPhrase = True
        if self.current_chunk:
            self.save_chunk(self.current_chunk)
            self.current_chunk = []
        print("END OF PHRASE")
        self.callFunc()

    def handsDown(self, leftHand, rightHand):
        """Check if both hands are below a certain threshold."""

        leftHandY = np.mean(
            [landmark['y'] for landmark in leftHand])
        rightHandY = np.mean(
            [landmark['y'] for landmark in rightHand])
        return leftHandY < HANDS_DOWN_THRESHOLD and rightHandY < HANDS_DOWN_THRESHOLD

    def callFunc(self):
        print("CALLING FUNCTION")
        # self.connectinator.phraseFlag = True
        self.reset()

    def reset(self):
        """Reset the state for the next real-time session."""
        self.pause_count = 0
        self.previous_keypoints = None
        self.current_chunk = []
        self.chunks = []
        self.word_boundaries = []
        self.buffer = []
        self.endOfPhrase = False
