import cv2
import mediapipe as mp
import numpy as np

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

video_path = 'signvideo/abdomen.mp4'
cap = cv2.VideoCapture(video_path)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

output_path = 'keypoints_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

FACE_LANDMARKS = [33, 263, 61, 291, 199, 1]  # Right eye, Left eye, nose, mouth corners

with mp_holistic.Holistic(static_image_mode=False, model_complexity=1) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        black_background = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = holistic.process(image_rgb)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                black_background, 
                results.pose_landmarks, 
                mp_holistic.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
            )

        if results.face_landmarks:
            for idx in FACE_LANDMARKS:
                landmark = results.face_landmarks.landmark[idx]
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                cv2.circle(black_background, (x, y), 2, (0, 255, 0), -1)

        if results.left_hand_landmarks:
            mp_drawing.draw_landmarks(
                black_background, 
                results.left_hand_landmarks, 
                mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
            )

        if results.right_hand_landmarks:
            mp_drawing.draw_landmarks(
                black_background, 
                results.right_hand_landmarks, 
                mp_holistic.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
            )

        out.write(black_background)

    cap.release()
    out.release()

print(f"Keypoints video saved as {output_path}")
