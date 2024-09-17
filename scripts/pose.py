import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose

class PoseExtractor:
    def __init__(self):
        self.pose = mp_pose.Pose()

    def extract_pose_keypoints(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        pose_keypoints = {}
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            for i in range(len(landmarks)):
                pose_keypoints[f"Pose_{i}"] = {
                    'x': landmarks[i].x,
                    'y': landmarks[i].y,
                    'z': landmarks[i].z
                }
        return pose_keypoints
