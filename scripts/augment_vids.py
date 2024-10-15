import pandas as pd
import random
from moviepy.editor import VideoFileClip
import os
import numpy as np
import glob

ISO_SIGN_PATH = r'data\New_Gloss_RGB_Data\New_Gloss_RGB_Data'
SIGNLE_SIGN_PATH = r'data\Signer\Signer'
FINAL_VIDEO_PATH = r'data\final_videos'

sign_numbers = pd.read_excel('datasignlist.xlsx', sheet_name="Stats") # this is just checker for data
iso_sign_index = pd.read_excel('datasignlist.xlsx', sheet_name="IsoSigns")
single_word_index = pd.read_excel('datasignlist.xlsx', sheet_name="SingleWord")

print(sign_numbers)
print(iso_sign_index)
print(single_word_index)

filenames = glob.glob(os.path.join(FINAL_VIDEO_PATH,"*_shaky_*.mp4"))

completed_vids = set([name.split("\\")[-1].split("_shaky_")[0] for name in filenames])

print(len(completed_vids))

failed_videos = []

def shaky_cam_effect(clip, shake_intensity_x, shake_intensity_y):
    def apply_shake(get_frame, t):
       # Get the current frame
        frame = get_frame(t)
        
        # Randomly select x and y shifts within the shake_intensity range
        x_shift = np.random.randint(-shake_intensity_x, shake_intensity_x)
        y_shift = np.random.randint(-shake_intensity_y, shake_intensity_y)
        
        # Apply the shift to the frame
        return np.roll(np.roll(frame, x_shift, axis=1), y_shift, axis=0)
    
    return clip.fl(apply_shake)

# Check how many entries are there add a shakcy cam one
def create_shaky_vids(df, og_vid_path):
    for index, row in df.iterrows(): #! can multi thread this loop
        print(index, row['Gloss'], row['Video_ID'])

        # When it break restarting form the same spot
        if str(row['Video_ID']) in completed_vids:
            continue

        max_number = 1
        # Creating difference amout for each work
        number_of_word = sign_numbers.loc[sign_numbers['unique_word'] == row['Gloss']]['occurances'].values[0]
        if number_of_word <= 1:
            max_number = 101
        elif number_of_word <= 5:
            max_number = 31
        elif number_of_word <= 10:
            max_number = 21
        elif number_of_word <= 20:
            max_number = 8
        elif number_of_word <= 60:
            max_number = 2
        elif number_of_word >= 125:
            max_number = 0

        # Creating og video path
        video_path = os.path.join(og_vid_path, str(row['Video_ID'])+'.mp4')
        try:
            video = VideoFileClip(video_path)
        except:
            failed_videos.append(str(row['Video_ID']))
            continue
        
        # Creating the abov enumber of shaky cam vids for each video
        for num in range(1, max_number):
            shake_x = num*10
            shake_y = num*30

            # Maxing at 12 cause otherwise to shaky
            if num > 12:
                shake_x =random.randint(1, 120)
                shake_y =random.randint(1, 300)

            # Altering the vid
            shaky_video = shaky_cam_effect(video, shake_intensity_x=shake_x, shake_intensity_y=shake_y)

            # Saving the video
            final_path = os.path.join(FINAL_VIDEO_PATH, str(row['Video_ID'])+f'_shaky_{str(num)}.mp4')
            shaky_video.write_videofile(final_path)

create_shaky_vids(iso_sign_index, ISO_SIGN_PATH)
create_shaky_vids(single_word_index, SIGNLE_SIGN_PATH)

with open('failed_ids.txt', 'a+') as f:
    for items in failed_videos:
        f.write('%s\n' %items)