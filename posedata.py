from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
import os

# Folder containing .pose files
folder_path = '/Users/albert/Downloads/Test'

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Process only .pose files
    if os.path.isfile(file_path) and filename.endswith('.pose'):
        # Read the pose file
        with open(file_path, "rb") as f:
            data_buffer = f.read()
            pose = Pose.read(data_buffer)

        # Create a visualizer object
        visualizer = PoseVisualizer(pose)

        # Generate output filenames based on input filename
        output_video_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_output.mp4")
        output_overlay_video_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_overlay_output.mp4")

        # Save the visualized poses as a video
        visualizer.save_video(output_video_path, visualizer.draw())

        # Optionally, save the overlay on the original video if available
        # Assuming the input video has the same name as the .pose file but with .mp4 extension
        input_video_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.mp4")
        if os.path.exists(input_video_path):
            visualizer.save_video(output_overlay_video_path, visualizer.draw_on_video(input_video_path))
        else:
            print(f"No matching video found for {filename}, skipping overlay creation.")

        print(f"Processed: {filename}")
