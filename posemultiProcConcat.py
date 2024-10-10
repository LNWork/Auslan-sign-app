from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from spoken_to_signed.gloss_to_pose import concatenate_poses  # Assuming concatenate_poses is from concatenate.py

# Function to process each .pose file individually
def process_pose_file(file_path):
    try:
        # Read the pose file
        with open(file_path, "rb") as f:
            data_buffer = f.read()
            pose = Pose.read(data_buffer)

        return pose  # Return the Pose object instead of processing it immediately
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Main function to process all files in parallel and concatenate
def process_all_files_in_parallel(folder_path):
    folder = Path(folder_path)
    
    # Get list of all .pose files in the folder
    pose_files = [str(file) for file in folder.glob("*.pose")]

    all_poses = []
    
    # Use ProcessPoolExecutor to load files in parallel
    with ProcessPoolExecutor() as executor:
        # Load all pose files concurrently
        results = executor.map(process_pose_file, pose_files)

    # Collect only valid Pose objects
    for pose in results:
        if pose is not None:
            all_poses.append(pose)

    # Check if there are enough poses to concatenate
    if len(all_poses) > 1:
        # Concatenate all poses
        concatenated_pose = concatenate_poses(all_poses)

        # Create a visualizer object for the concatenated pose
        visualizer = PoseVisualizer(concatenated_pose)

        # Save the visualized concatenated poses as a video
        output_video_path = os.path.join(folder_path, "concatenated_output.mp4")
        visualizer.save_video(output_video_path, visualizer.draw())

        print("Processed and concatenated all pose files.")
    else:
        print("Not enough .pose files to concatenate.")

if __name__ == "__main__":
    folder_path = '/Users/albert/Downloads/Test'
    process_all_files_in_parallel(folder_path)
