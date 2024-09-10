import cv2
import os
# This is the script for the gloss single word video augmentation. Let Kabilan know if this doesn't work properly


#READ THIS probably won't work because i had each of the videos on it so I need to work around how to link it to the videos but it does augment 


#frame by frame breakdown extract frames, apply image aug to frame, reassemble, pray it works
# if testing test with smaller size videos or you will be there forever  
# Path to the folder containing the original videos locally 
# I am going to see if I can do it through a google drive link or we just do it locally
input_folder = "C:/Users/kabil/Downloads/New_Gloss_RGB_Data/"

# Path where the augmented videos will be saved
output_folder = "C:/Users/kabil/Downloads/Augmented_Videos/"

# Create the output folder if it doesn't already exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# List all video files in the input folder with .mp4 extension
videos = [f for f in os.listdir(input_folder) if f.endswith('.mp4')]

# Scaling factor for zoom by 20% feel free to change it
scale_factor = 1.2

# Loop through each video in the input folder
for video in videos:
    video_path = os.path.join(input_folder, video)
    print(f"Processing video: {video}")

    # Open the video file for reading
    cap = cv2.VideoCapture(video_path)

    # Get the video's original width, height, and frames per second (fps)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate the new width and height for zooming (based on the scale factor)
    new_width = int(frame_width / scale_factor)
    new_height = int(frame_height / scale_factor)

    # Define the codec and create a videowriter object to save the augmented video
    output_path = os.path.join(output_folder, f"aug_{video}")
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Process each frame of the video
    while cap.isOpened():
        ret, frame = cap.read()

        # If the frame was not read correctly, break the loop (end of video)
        if not ret:
            break

        # Get the center of the frame for cropping (zooming effect)
        center_x, center_y = frame_width // 2, frame_height // 2
        
        # Calculate the top-left coordinates of the cropped region
        x1 = center_x - new_width // 2
        y1 = center_y - new_height // 2

        # Crop the frame to the new dimensions (zoomed in)
        zoomed_frame = frame[y1:y1 + new_height, x1:x1 + new_width]

        # Resize the zoomed frame back to the original video dimensions
        zoomed_frame = cv2.resize(zoomed_frame, (frame_width, frame_height))

        # Augmentation: Flip the zoomed frame horizontally 
        augmented_frame = cv2.flip(zoomed_frame, 1)

        out.write(augmented_frame)

    # Release the video capture and writer objects
    cap.release()
    out.release()

    # Indicate that processing for the current video is finished
    print(f"Finished processing: {video}")

print("BEES")


        # Rotation:  rotating the image
        # angle = np.random.uniform(-30, 30)  # Random angle from -30 30
        # center = (frame_width // 2, frame_height // 2)
        # matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        # rotated_frame = cv2.warpAffine(augmented_frame, matrix, (frame_width, frame_height))

        # Scaling: zoom in/ out of the imagefor different distances
        # scale_factor = np.random.uniform(0.8, 1.2)  # random scale between 0.8 and 1.2
        # new_width = int(frame_width / scale_factor)
        # new_height = int(frame_height / scale_factor)
        # zoomed_frame = cv2.resize(augmented_frame, (new_width, new_height))
        # zoomed_frame = cv2.resize(zoomed_frame, (frame_width, frame_height))

        # Translation: move image left, right up  down
        # tx = np.random.uniform(-50, 50)  # shift in x-direction
        # ty = np.random.uniform(-50, 50)  # shift in y-direction
        # translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        # translated_frame = cv2.warpAffine(augmented_frame, translation_matrix, (frame_width, frame_height))

        # Brightness/cntrast Adjustments: change brightness and contrast
        # brightness = np.random.uniform(0.5, 1.5)  # rand brightness factor
        # contrast = np.random.uniform(0.5, 1.5)    # rand contrast factor
        # adjusted_frame = cv2.convertScaleAbs(augmented_frame, alpha=contrast, beta=brightness)

        # noise injection adding noise no clue if this works to be honest just try it out
        # noise = np.random.normal(0, 25, augmented_frame.shape).astype(np.uint8)
        # noisy_frame = cv2.add(augmented_frame, noise)

        # Uncomment the one you are using and change it  `augmented_frame` with the processed frame
        # out.write(rotated_frame)         # For rotation
        # out.write(zoomed_frame)          # For scaling
        # out.write(translated_frame)      # For translation
        # out.write(adjusted_frame)        # For brightness/contrast 
        # out.write(noisy_frame)           # For noise injection