import os
import subprocess
from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer

# Paths
input_folder = r"C:\Users\kabil\Downloads\signvideo"  # Folder containing videos
output_folder = r"C:\Users\kabil\Downloads\signvideo"  # Folder to save pose files and visualizations

# Process each video file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".mp4"):  # Process only mp4 files
        video_path = os.path.join(input_folder, filename)
        
        # Define the output pose file name
        pose_file_name = filename.replace(".mp4", ".pose")
        pose_file_path = os.path.join(output_folder, pose_file_name)
        
        # Generate pose file using the command line
        subprocess.run([
            "video_to_pose",  # Ensure this command is available in your PATH
            "--format", "mediapipe",
            "-i", video_path,
            "-o", pose_file_path
        ])
        
        # Load the pose data
        with open(pose_file_path, "rb") as data_buffer:
            pose = Pose.read(data_buffer.read())
        
        # Create a visualizer object
        visualizer = PoseVisualizer(pose)

        # Save the visualized poses as a video
        visualizer.save_video(os.path.join(output_folder, f"{pose_file_name.replace('.pose', 'output_video.mp4')}"), visualizer.draw())

print("DOne")