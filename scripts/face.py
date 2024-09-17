import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

class FaceMeshExtractor:
    def __init__(self):
        self.face_mesh = mp_face_mesh.FaceMesh()

    def extract_face_keypoints(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(frame_rgb)
        face_keypoints = {}
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                for i, landmark in enumerate(face_landmarks.landmark):
                    face_keypoints[f"Face_{i}"] = {
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    }
        return face_keypoints
