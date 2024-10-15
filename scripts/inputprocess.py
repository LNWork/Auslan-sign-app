import os  # Import os to handle directory operations
import json
import numpy as np

# Parameters (adjust for real-time speed and accuracy)
THRESHOLD = 0.05  # 5% change in keypoints
VISIBILITY_THRESHOLD = 0.6  # Minimum visibility for a keypoint to be considered
VISIBILITY_COUNT = 0.7  # Minimum percentage of keypoints with visibility above threshold
WINDOW_SIZE = 30   # Number of frames with little to no movement to consider a pause


class RealTimeBoundaryDetector:
    def __init__(self, threshold=THRESHOLD, window_size=WINDOW_SIZE, buffer_size=5):
        self.threshold = threshold
        self.window_size = window_size
        self.buffer_size = buffer_size  # Add buffer size for lookahead
        self.pause_count = 0
        self.previous_keypoints = None
        self.word_boundaries = []
        self.current_chunk = []
        self.chunks = []
        self.buffer = []  # Buffer to hold frames temporarily
        self.chunk_counter = 0

    def extract_keypoints(self, landmarks):
        """Extract the keypoints (x, y, z, visibility) from the landmarks."""
        if not isinstance(landmarks, list):
            print("Expected landmarks to be a list, received:", type(landmarks))
            # Return an empty array if input is invalid
            return np.empty((0, 4))
        try:
            return np.array([[landmark['x'], landmark['y'], landmark['z'], landmark['visibility']] for landmark in landmarks])
        except KeyError as e:
            print(f"Missing key in landmark: {e}")
            # Return an empty array if a key is missing
            return np.empty((0, 4))

    def combine_keypoints(self, frame):
        """Combine pose, left hand, and right hand keypoints into a single array."""
        pose = self.extract_keypoints(frame['pose_landmarks'])
        left_hand = self.extract_keypoints(frame['left_hand_landmarks'])
        right_hand = self.extract_keypoints(frame['right_hand_landmarks'])

        # Concatenate pose, left hand, and right hand keypoints
        return np.concatenate((pose, left_hand, right_hand), axis=0)

    def calculate_velocity(self, keypoints_current, keypoints_previous):
        """Calculate the velocity of keypoints between two frames."""
        velocities = np.linalg.norm(
            keypoints_current[:, :3] - keypoints_previous[:, :3], axis=1)
        return np.mean(velocities)  # Return average velocity of all keypoints

    def process_frame(self, frame):
        """Process a single frame of keypoint data in real-time."""
        keypoints_current = self.combine_keypoints(frame)

        # Add concatenated keypoints to a new 'data' field in the frame
        # Store combined keypoints in 'data' field
        frame['data'] = keypoints_current.tolist()

        if self.previous_keypoints is not None:
            # Calculate velocity (movement) between consecutive frames
            velocity = self.calculate_velocity(
                keypoints_current, self.previous_keypoints)

            # Debugging output
            print(
                f"Processing frame: {frame['frame']}, Velocity: {velocity}, Pause Count: {self.pause_count}")

            # Check if movement is below the threshold and visibility is low
            if velocity < self.threshold and not self.visibility_check(keypoints_current):
                self.pause_count += 1
                print(f"Pause count increased to: {self.pause_count}")
            else:
                self.pause_count = 0  # Reset if significant movement is detected

            # Check if we detect a potential boundary
            if self.pause_count >= self.window_size:
                self.buffer.append(frame)  # Add frame to the buffer

                # Debugging: Check contents of buffer
                print(f"Buffer contents: {[f['frame'] for f in self.buffer]}")

                if len(self.buffer) >= self.buffer_size:
                    if all(self.calculate_velocity(self.combine_keypoints(f), self.previous_keypoints) < self.threshold for f in self.buffer):
                        avg_velocity = np.mean([self.calculate_velocity(
                            self.combine_keypoints(f), self.previous_keypoints) for f in self.buffer])
                        if avg_velocity < self.threshold:
                            self.word_boundaries.append(
                                frame.get('frame', len(self.word_boundaries)))
                            self.chunks.append(self.current_chunk)
                            # Save chunk here
                            self.save_chunk(self.current_chunk)
                            self.current_chunk = []
                            self.pause_count = 0
                            self.buffer = []
                    else:
                        self.buffer = []  # Clear the buffer if movement is detected
            else:
                self.buffer = []  # Clear the buffer if movement is detected

        # Add the current frame to the chunk
        self.current_chunk.append(frame)
        # Update the previous frame's keypoints
        self.previous_keypoints = keypoints_current

    def save_chunk(self, chunk):
        """Save the current chunk to a JSON file in the specified format."""
        os.makedirs('outputChunks',
                    exist_ok=True)  # Ensure the output directory exists
        filename = f"outputChunks/chunk_{self.chunk_counter}.json"

        # Prepare the formatted data
        chunk_data = []
        for frame in chunk:
            chunk_data.append({
                # Get frame number, default to -1 if not available
                "frame": frame.get('frame', -1),
                # The concatenated pose, left_hand, and right_hand keypoints
                "data": frame['data']
            })

        # Save to the JSON file
        with open(filename, 'w') as f:
            json.dump(chunk_data, f, indent=4)

        print(f"Chunk saved to {filename}")
        self.chunk_counter += 1

    def visibility_check(self, keypoints):
        """Check if the visibility of keypoints is above a threshold."""
        visible_keypoints_count = (
            keypoints[..., 3] >= VISIBILITY_THRESHOLD).sum()
        total_keypoints = len(keypoints[..., 3])

        # Check if the visible keypoints meet the required percentage
        return visible_keypoints_count >= total_keypoints * VISIBILITY_COUNT

    def reset(self):
        """Reset the state for the next real-time session."""
        self.pause_count = 0
        self.previous_keypoints = None
        self.current_chunk = []
        self.chunks = []
        self.word_boundaries = []


def main():
    real_time_detector = RealTimeBoundaryDetector()

    # Load multiple frames from the JSON file
    frames = load_multiple_frames('thank_you_auslan_keypoints.json')

    if frames is None:
        print("No frames to process.")
        return

    # Process each frame in sequence (simulating real-time streaming)
    for frame in frames:
        real_time_detector.process_frame(frame)

    # After processing all frames, check remaining chunk (if any)
    if real_time_detector.current_chunk:
        real_time_detector.save_chunk(real_time_detector.current_chunk)

    print("Processing complete.")
    print(f"Detected word boundaries: {real_time_detector.word_boundaries}")
    print(f"Number of chunks saved: {real_time_detector.chunk_counter}")


def load_multiple_frames(filepath):
    """Simulate real-time data by reading multiple frames from the text file."""
    with open(filepath, 'r') as f:
        try:
            # Load all frames from the file as a JSON object
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print("Unexpected data format. Expected a list of frames.")
                return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None


if __name__ == "__main__":
    main()
