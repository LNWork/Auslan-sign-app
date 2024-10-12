from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
import os
import cv2
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
    valid_filenames = []
    
    # Use ProcessPoolExecutor to load files in parallel
    with ProcessPoolExecutor() as executor:
        # Load all pose files concurrently
        results = executor.map(process_pose_file, pose_files)

    # Collect only valid Pose objects and their corresponding filenames
    for pose, filename in zip(results, pose_files):
        if pose is not None:
            all_poses.append(pose)
            valid_filenames.append(os.path.splitext(os.path.basename(filename))[0])

    # Check if there are enough poses to concatenate
    if len(all_poses) > 1:
        # Concatenate all poses and get frame ranges with filenames
        concatenated_pose, frame_ranges = concatenate_poses(all_poses, valid_filenames)

        # Create a visualizer object for the concatenated pose
        visualizer = PoseVisualizer(concatenated_pose)

        # Save the visualized concatenated poses as a video
        output_video_path = os.path.join(folder_path, "concatenated_output.mp4")

        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Define the codec
        video_writer = cv2.VideoWriter(output_video_path, fourcc, concatenated_pose.body.fps, 
                                       (concatenated_pose.header.dimensions.width, concatenated_pose.header.dimensions.height))

        # Draw the pose and overlay the filenames for each frame
        for frame in visualizer.draw_frame_with_filename(frame_ranges):
            video_writer.write(frame)  # Save the frame to the video

        video_writer.release()  # Finalize and close the video file
        print(f"Processed and concatenated all pose files into {output_video_path}.")
    else:
        print("Not enough .pose files to concatenate.")

if __name__ == "__main__":
    folder_path = '/Users/albert/Downloads/Test'
    process_all_files_in_parallel(folder_path)
