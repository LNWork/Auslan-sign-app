import cv2
import mediapipe as mp
import numpy as np
import os
import json

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=2)

video_folder = "signvideo"
video_filename = "abdomen.mp4"  
video_path = os.path.join(video_folder, video_filename)

pose_output_file = "abdomen_pose_data.json"

def extract_pose_data(video_path, output_file, visualize=False):
    if not os.path.exists(video_path):
        print(f"Error: Video file {video_path} not found.")
        return

    cap = cv2.VideoCapture(video_path)
    pose_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame 
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = pose.process(rgb_frame)

        if result.pose_landmarks:
            # Extract keypoints
            keypoints = [(lm.x, lm.y, lm.z) for lm in result.pose_landmarks.landmark]
            pose_data.append(keypoints)

        if visualize:
            mp.solutions.drawing_utils.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.imshow('Pose Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Save pose data as JSON
    with open(output_file, 'w') as f:
        json.dump(pose_data, f) 


    cap.release()
    cv2.destroyAllWindows()

# Call the function to proces video
extract_pose_data(video_path, pose_output_file, visualize=True)
print(f"Pose data saved as {pose_output_file}")
