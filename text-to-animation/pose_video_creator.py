import os
import tempfile
import json
import firebase_admin
from firebase_admin import credentials, storage
from pose_format import Pose
from pose_format.pose_visualizer import PoseVisualizer
import io
import cv2
from concurrent.futures import ProcessPoolExecutor
from spoken_to_signed.gloss_to_pose import concatenate_poses
from dotenv import load_dotenv


# Required for subprocess.run
import subprocess

# Load environment variables from the .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'app', '.env'))


# Retrieve credentials from environment variables
firebase_credentials = {
    "type": os.getenv("FIREBASE_TYPE"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID"),
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY"),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
    "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL"),
    "universe_domain": os.getenv("FIREBASE_UNIVERSE_DOMAIN")
}

# Check if any credential is missing
if None in firebase_credentials.values():
    raise ValueError("Firebase credentials not found in .env file.")

# Initialize Firebase Admin SDK
cred = credentials.Certificate(firebase_credentials)
firebase_admin.initialize_app(
    cred, {'storageBucket': 'auslan-194e5.appspot.com'})

# Process pose file from Firebase Storage

def process_pose_file(blob_name):
    try:
        bucket = storage.bucket()
        # Assuming each word corresponds to a .pose file
        blob = bucket.blob(f"{blob_name}.pose")
        if not blob.exists():
            print(f"Blob {blob_name} does not exist.")
            return None

        data_buffer = io.BytesIO()
        blob.download_to_file(data_buffer)
        data_buffer.seek(0)
        pose = Pose.read(data_buffer.read())
        return pose
    except Exception as e:
        print(f"Error processing {blob_name}: {e}")
        return None

# Concatenate poses and upload the video back to Firebase
def concatenate_poses_and_upload(blob_names, sentence):
    all_poses = []
    valid_filenames = []

    with ProcessPoolExecutor() as executor:
        results = executor.map(process_pose_file, blob_names)

    for pose, blob_name in zip(results, blob_names):
        if pose:
            all_poses.append(pose)
            valid_filenames.append(os.path.splitext(os.path.basename(blob_name))[0])

    if len(all_poses) > 1:
        concatenated_pose, frame_ranges = concatenate_poses(all_poses, valid_filenames)
        visualizer = PoseVisualizer(concatenated_pose)

        # Create a temporary file to store the video
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_video_path = temp_video.name

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(temp_video_path, fourcc, concatenated_pose.body.fps,
                                       (concatenated_pose.header.dimensions.width, concatenated_pose.header.dimensions.height))

        for frame in visualizer.draw_frame_with_filename(frame_ranges):
            video_writer.write(frame)

        video_writer.release()
        temp_video.close()
        
        # Convert the video to a more compatible format
        # (some video players may not support the default format)
        outputPath = temp_video_path.replace('.mp4', '_converted.mp4')
        # subprocess will run using the host computer
        subprocess.run(['ffmpeg', '-i', temp_video_path, '-vcodec',
                       'libx264', '-acodec', 'aac', outputPath])

        # Upload the video to Firebase Storage in the 'output_videos/' folder with the sentence as the filename
        bucket = storage.bucket()
        blob = bucket.blob(f"output_videos/{sentence}.mp4")  # Updated path
        blob.upload_from_filename(temp_video_path, content_type="video/mp4")

        # Optionally make the file publicly accessible (if needed)
        blob.make_public()
        print(f"Video uploaded to Firebase at 'output_videos/{sentence}.mp4' and accessible at: {blob.public_url}")

        # Remove the temporary file after uploading
        os.remove(temp_video_path)
    else:
        print("Not enough .pose files to concatenate")


# Check if a word has a corresponding pose file in Firebase
def get_valid_blobs_from_sentence(sentence):
    words = [word.capitalize() for word in sentence.split()]
    valid_blob_names = []

    bucket = storage.bucket()

    for word in words:
        blob = bucket.blob(f"{word}.pose")
        if blob.exists():
            valid_blob_names.append(word)
        else:
            print(
                f"Skipping word '{word}', no corresponding .pose file found.")

    return valid_blob_names


def process_sentence(sentence):
    # Get valid blob names (i.e., words that have a corresponding .pose file)
    valid_blob_names = get_valid_blobs_from_sentence(sentence)

    if len(valid_blob_names) == 0:
        print("No valid words found with corresponding .pose files.")
        return None

    # Get the path to the temporary video file
    temp_video_path = concatenate_poses_and_upload(valid_blob_names, sentence)

    if temp_video_path:
        print(f"Video saved at {temp_video_path}")
        return temp_video_path
    else:
        print("Not enough .pose files to concatenate")
        return None


if __name__ == "__main__":
    # Example usage: replace with actual API response
    api_response_sentence = "france wales africa"
    process_sentence(api_response_sentence)
