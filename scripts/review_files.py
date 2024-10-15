import pandas as pd
import os
import numpy as np
import glob
import shutil

ALL_JSON = r'data/json_keypoints'

filepaths = glob.glob(os.path.join(ALL_JSON, "*.json"))

sign_numbers = pd.read_excel('datasignlist.xlsx', sheet_name="Stats") # this is just checker for data
sign_numbers['number_vids'] = 0
sign_numbers['shaky_number'] = 0
iso_sign_index = pd.read_excel('datasignlist.xlsx', sheet_name="IsoSigns")
single_word_index = pd.read_excel('datasignlist.xlsx', sheet_name="SingleWord")

full_gloss = pd.concat([iso_sign_index, single_word_index])[['Gloss', 'Video_ID']]
full_gloss = full_gloss.astype(str)


#print(filepaths)
counter = 0
for file in filepaths:
    wholefilename = file.split("\\")[-1]

    if 'shaky' in file: 
        file_name = wholefilename.split("_shaky_")[0].replace(".json", "")
        shaky = True
    else:
        file_name = wholefilename.split("_keypoints")[0].replace(".json", "")
        shaky = False
    
    row = full_gloss.loc[full_gloss['Video_ID'] == file_name]

    word = row['Gloss'].values[0]

    sign_numbers.loc[sign_numbers['unique_word'] == word, 'number_vids'] += 1

    if shaky:
        sign_numbers.loc[sign_numbers['unique_word'] == word, 'shaky_number'] += 1


sign_numbers.to_excel('final_stats.xlsx', index=False)