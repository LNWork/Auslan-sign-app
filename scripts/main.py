import cv2
import json
import os
from pose_extraction import PoseExtractor
from face_mesh_extraction import FaceMeshExtractor
from hands_extraction import HandsExtractor

def extract_keypoints(video_path):
    pose_extractor = PoseExtractor()
    face_mesh_extractor = FaceMeshExtractor()
    hands_extractor = HandsExtractor()

    all_keypoints_data = []
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return all_keypoints_data

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        pose_keypoints = pose_extractor.extract_pose_keypoints(frame)
        face_keypoints = face_mesh_extractor.extract_face_keypoints(frame)
        hands_keypoints = hands_extractor.extract_hands_keypoints(frame)
        
        frame_keypoints = {
            "Pose": pose_keypoints,
            "Face": face_keypoints,
            "Hands": hands_keypoints
        }
        all_keypoints_data.append(frame_keypoints)
    
    cap.release()
    print(f"Extracted keypoints from {video_path}")
    return all_keypoints_data

def save_keypoints_to_json(all_keypoints_data, output_path):
    with open(output_path, 'w') as f:
        json.dump(all_keypoints_data, f, indent=4)
    print(f"Keypoints data has been saved to {output_path}")

if __name__ == "__main__":
    video_folder = 'C:\\Users\\kabil\\Videos\\signertest'
    output_file = 'C:\\Users\\kabil\\Downloads\\mediapipeattempt1\\keypoints_data.json'
    
    all_keypoints_data = {}
    for video_file in os.listdir(video_folder):
        if video_file.endswith('.mp4'):
            video_path = os.path.join(video_folder, video_file)
            keypoints_data = extract_keypoints(video_path)
            all_keypoints_data[video_file] = keypoints_data
    
    save_keypoints_to_json(all_keypoints_data, output_file)
