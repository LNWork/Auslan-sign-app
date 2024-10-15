import cv2
import mediapipe as mp
import json
import os
from glob import glob
from concurrent.futures import ProcessPoolExecutor

# Initialize Model
mp_holistic = mp.solutions.holistic

# Directories for input and output
input_dir = 'data\\all_single_vids'  # Change this to your directory with videos
output_dir = 'data\\json_keypoints'  # Directory to save JSON files

# Make sure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# List Video files
video_files = glob(os.path.join(input_dir, '*.mp4'))  # Change extension if needed

def process_video(video_file):
    # Extract video name
    video_name = os.path.splitext(os.path.basename(video_file))[0]
    
    # Open the video file
    cap = cv2.VideoCapture(video_file)
    
    # Initialize dictionary to store keypoints for each frame
    keypoints_data = []

    # Initialize the Holistic model
    with mp_holistic.Holistic(static_image_mode=False, 
                              model_complexity=1, 
                              smooth_landmarks=True, 
                              min_detection_confidence=0.5, 
                              min_tracking_confidence=0.5) as holistic:
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the BGR frame to RGB for Mediapipe processing
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame with the Holistic model
            results = holistic.process(frame_rgb)

            # Initialize a dictionary for the current frame's keypoints
            frame_keypoints = {'frame': frame_idx}

            # Extract pose landmarks
            pose_number = 33
            hand_number = 21
            if results.pose_landmarks:
                frame_keypoints['data'] = [{'x': lm.x, 'y': lm.y, 'z': lm.z, 'visibility': lm.visibility} 
                                            for lm in results.pose_landmarks.landmark]
            else:
                frame_keypoints['data'] = [{'x': 0, 'y': 0, 'z': 0, 'visibility': 0} 
                                            for _ in range(pose_number)]

            # Extract left_hand landmarks
            if results.left_hand_landmarks:
                frame_keypoints['data'] += [{'x': lm.x, 'y': lm.y, 'z': lm.z, 'visibility': lm.visibility} 
                                             for lm in results.left_hand_landmarks.landmark]
            else:
                frame_keypoints['data'] += [{'x': 0, 'y': 0, 'z': 0, 'visibility': 0} 
                                             for _ in range(hand_number)]

            # Extract right_hand landmarks
            if results.right_hand_landmarks:
                frame_keypoints['data'] += [{'x': lm.x, 'y': lm.y, 'z': lm.z, 'visibility': lm.visibility} 
                                             for lm in results.right_hand_landmarks.landmark]
            else:
                frame_keypoints['data'] += [{'x': 0, 'y': 0, 'z': 0, 'visibility': 0} 
                                             for _ in range(hand_number)]

            # keypoint data append, increment frame
            keypoints_data.append(frame_keypoints)
            frame_idx += 1
            
    json_output_path = os.path.join(output_dir, f"{video_name}_keypoints.json")
    with open(json_output_path, 'w') as f:
        json.dump(keypoints_data, f, indent=4)

    cap.release()
    return video_name

if __name__ == '__main__':
    # Use ProcessPoolExecutor for parallel processing
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(process_video, video_files))

    print(f"Collected Keypoints from {len(results)} Videos")