import cv2
import mediapipe as mp
import json

# Initialize MediaPipe Holistic and Drawing utilities
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Function to convert landmarks to a list of dictionaries
def extract_landmarks(landmarks):
    return [{'x': lm.x, 'y': lm.y, 'z': lm.z, 'visibility': lm.visibility} for lm in landmarks.landmark]

# Open the video file
cap = cv2.VideoCapture('file path goes here')

# Initialize dictionary to store keypoints for each frame
keypoints_data = []

# Initialize Holistic
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
        if results.pose_landmarks:
            frame_keypoints['pose_landmarks'] = extract_landmarks(results.pose_landmarks)
        
        # Extract face landmarks
        if results.face_landmarks:
            frame_keypoints['face_landmarks'] = extract_landmarks(results.face_landmarks)

        # Extract left hand landmarks
        if results.left_hand_landmarks:
            frame_keypoints['left_hand_landmarks'] = extract_landmarks(results.left_hand_landmarks)
        
        # Extract right hand landmarks
        if results.right_hand_landmarks:
            frame_keypoints['right_hand_landmarks'] = extract_landmarks(results.right_hand_landmarks)

        # Append the frame data to keypoints_data
        keypoints_data.append(frame_keypoints)

        # Optionally draw landmarks on the frame (optional visualization)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        if results.face_landmarks:
            mp_drawing.draw_landmarks(frame, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION)
        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Show the frame (optional)
        cv2.imshow('Holistic Model Output', frame)

        # Exit with 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        # Increment frame index
        frame_idx += 1

# Save the keypoints data as a JSON file
with open('keypoints_data.json', 'w') as f:
    json.dump(keypoints_data, f, indent=4)

# Release video capture and close windows
cap.release()
cv2.destroyAllWindows()