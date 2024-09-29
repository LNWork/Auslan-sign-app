import os
import json
import cv2
import numpy as np
from pose_format.pose import Pose  
from pose_format.pose_visualizer import PoseVisualizer 

def load_pose_from_dict(pose_data):
    print("Loaded pose data structure:", type(pose_data), pose_data)

    if isinstance(pose_data, list):
        if len(pose_data) > 0 and isinstance(pose_data[0], list):
            pose_data = pose_data[0]  
        else:
            print("Unexpected data format, exiting.")
            return

video_folder = "signvideo"
video_filename = "abdomen.mp4"  
video_path = os.path.join(video_folder, video_filename)

pose_data_file = "abdomen_pose_data.json"  
with open(pose_data_file, 'r') as f:
    pose_data = json.load(f)

def process_video(video_path):
   
    p = load_pose_from_dict(pose_data)

  
    scale = p.header.dimensions['width'] / 256 
    p.header.dimensions['width'] = int(p.header.dimensions['width'] / scale)
    p.header.dimensions['height'] = int(p.header.dimensions['height'] / scale)
    p.body.data = p.body.data / scale

 
    v = PoseVisualizer(p)

    gif_filename = f"{os.path.splitext(video_filename)[0]}_stick_figure.gif"
    v.save_gif(gif_filename, v.draw())
    print(f"GIF saved as {gif_filename}")

process_video(video_path)
