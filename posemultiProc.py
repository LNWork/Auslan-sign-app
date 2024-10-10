from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

# Function to process each .pose file
def process_pose_file(file_path):
    try:
        # Read the pose file
        with open(file_path, "rb") as f:
            data_buffer = f.read()
            pose = Pose.read(data_buffer)

        # Create a visualizer object
        visualizer = PoseVisualizer(pose)

        # Generate output filenames based on input filename
        output_video_path = os.path.splitext(file_path)[0] + "_output.mp4"
        # output_overlay_video_path = os.path.splitext(file_path)[0] + "_overlay_output.mp4"

        # Save the visualized poses as a video
        visualizer.save_video(output_video_path, visualizer.draw())

        # # Optionally, save the overlay on the original video if available
        # input_video_path = os.path.splitext(file_path)[0] + ".mp4"
        # if os.path.exists(input_video_path):
        #     visualizer.save_video(output_overlay_video_path, visualizer.draw_on_video(input_video_path))
        # else:
        #     print(f"No matching video found for {file_path}, skipping overlay creation.")

        print(f"Processed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Main function to process all files in parallel
def process_all_files_in_parallel(folder_path):
    folder = Path(folder_path)
    
    # Get list of all .pose files in the folder
    pose_files = [str(file) for file in folder.glob("*.pose")]

    # Use ProcessPoolExecutor to process files in parallel
    with ProcessPoolExecutor() as executor:
        executor.map(process_pose_file, pose_files)

if __name__ == "__main__":
    folder_path = '/Users/albert/Downloads/Test'
    process_all_files_in_parallel(folder_path)