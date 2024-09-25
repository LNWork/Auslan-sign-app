import numpy as np

# Parameters (adjust for real-time speed and accuracy)
THRESHOLD = 0.06  # 5% change in keypoints
WINDOW_SIZE = 6   # Number of frames with little to no movement to consider a pause


class RealTimeBoundaryDetector:
    def __init__(self, threshold=THRESHOLD, window_size=WINDOW_SIZE):
        self.threshold = threshold
        self.window_size = window_size
        self.pause_count = 0
        self.previous_keypoints = None
        self.word_boundaries = []
        self.current_chunk = []
        self.chunks = []

    def extract_keypoints(self, landmarks):
        """Extract the keypoints (x, y, z) from the landmarks."""
        return np.array([[landmark['x'], landmark['y'], landmark['z']] for landmark in landmarks])

    def calculate_velocity(self, keypoints_current, keypoints_previous):
        """Calculate the velocity of keypoints between two frames."""
        velocities = np.linalg.norm(
            keypoints_current - keypoints_previous, axis=1)
        return np.mean(velocities)  # Return average velocity of all keypoints

    def process_frame(self, frame):
        """Process a single frame of data in real-time."""
        pose_keypoints_current = self.extract_keypoints(
            frame['pose_landmarks'])

        # Handle empty left and right hand landmarks
        left_hand_keypoints_current = self.extract_keypoints(
            frame.get('left_hand_landmarks', []))
        right_hand_keypoints_current = self.extract_keypoints(
            frame.get('right_hand_landmarks', []))

        # If hand landmarks are empty, create dummy arrays with shape (21, 3)
        if left_hand_keypoints_current.size == 0:
            left_hand_keypoints_current = np.zeros(
                (21, 3))  # Assuming (x, y, z)
        if right_hand_keypoints_current.size == 0:
            right_hand_keypoints_current = np.zeros(
                (21, 3))  # Same here for right hand

        # Combine all keypoints into one array
        keypoints_current = np.concatenate(
            (pose_keypoints_current, left_hand_keypoints_current,
             right_hand_keypoints_current), axis=0
        )

        if self.previous_keypoints is not None:
            # Calculate velocity (movement) between consecutive frames
            velocity = self.calculate_velocity(
                keypoints_current, self.previous_keypoints)

            # If velocity is below the threshold, increase pause count
            if velocity < self.threshold:
                self.pause_count += 1
            else:
                self.pause_count = 0  # Reset if significant movement detected

            # If the pause count exceeds the window size, mark a word boundary
            if self.pause_count >= self.window_size:
                self.word_boundaries.append(frame['frame'])
                self.chunks.append(self.current_chunk)  # Save current chunk
                self.current_chunk = []  # Start a new chunk
                self.pause_count = 0  # Reset pause counter

        self.current_chunk.append(frame)  # Add frame to the current chunk
        self.previous_keypoints = keypoints_current  # Update previous frame

    def get_chunks(self):
        """Return chunks of frames between word boundaries."""
        return self.chunks

    def reset(self):
        """Reset the state for the next real-time session."""
        self.pause_count = 0
        self.previous_keypoints = None
        self.current_chunk = []
        self.chunks = []
        self.word_boundaries = []

# Real-time simulation example (using a stream of frames)


def main():
    # Example: Simulate a real-time frame stream from JSON data
    real_time_detector = RealTimeBoundaryDetector()

    # Simulate a sequence of frames
    frames = load_json_data('scripts/combined_output.json')

    for frame in frames:
        real_time_detector.process_frame(frame)

    # Access detected word boundaries and chunks
    chunks = real_time_detector.get_chunks()
    print("Detected word boundaries at frames:",
          real_time_detector.word_boundaries)
    print("Number of chunks detected:", len(chunks))
    print("Number of frames in data:", len(frames))

    # For real-time applications, after processing each chunk, send it to the model
    # Here, chunks can be passed to a machine learning model or processed further
    # Example: pass_chunk_to_model(chunks[-1])


def load_json_data(filepath):
    """Simulate real-time JSON data input."""
    import json
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    main()
