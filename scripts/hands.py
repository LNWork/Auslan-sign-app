import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

class HandsExtractor:
    def __init__(self):
        self.hands = mp_hands.Hands()

    def extract_hands_keypoints(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        hands_keypoints = {}
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i, landmark in enumerate(hand_landmarks.landmark):
                    hands_keypoints[f"Hand_{i}"] = {
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    }
        return hands_keypoints
