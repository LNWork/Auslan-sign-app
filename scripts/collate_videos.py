import pandas as pd
import os
import numpy as np
import glob
import shutil

ISO_SIGN_PATH = r'data\New_Gloss_RGB_Data\New_Gloss_RGB_Data'
SIGNLE_SIGN_PATH = r'data\Signer\Signer'
FINAL_VIDEO_PATH = r'data\final_videos'

FINAL_VID_LOC = r'data\all_single_vids'

sign_numbers = pd.read_excel('datasignlist.xlsx', sheet_name="Stats") # this is just checker for data
iso_sign_index = pd.read_excel('datasignlist.xlsx', sheet_name="IsoSigns")
single_word_index = pd.read_excel('datasignlist.xlsx', sheet_name="SingleWord")

filenames = glob.glob(os.path.join(SIGNLE_SIGN_PATH, "*.mp4"))

print(len(filenames))

vid_names = single_word_index['Video_ID'].values

for filename in filenames:
    file_name = filename.split('\\')[-1]
    f_name = file_name.replace(".mp4", "")
    print(f_name)

    if f_name in vid_names:
        new_path = os.path.join(FINAL_VID_LOC, file_name)

        shutil.move(filename, new_path)
