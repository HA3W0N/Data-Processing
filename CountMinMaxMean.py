import sys
import cv2
import glob
import os
import random
import numpy as np

if __name__ == "__main__":
    frame_list = []
    metadata_file = "DataCorruption.txt"
    with open(metadata_file, "w")as f:
        f.write("Metadata of Data Corruption with Pixel-Downsample/Drop/Noise\n")
    # Use os.walk to traverse through all subfolders
    for root, dirs, files in os.walk('.'):
    # Use glob to filter only .mp4 files
        mp4_files = list(glob.glob(os.path.join(root, '*.mp4')))
        for videos in mp4_files:
            video = cv2.VideoCapture(videos)
            frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
            frame_list.append(frame)
            video.release()
    
    print("There is {} mp4 files, Maximum frame : {}, Minimum frame : {} , Mean : {} ".format(len(frame_list), max(frame_list), min(frame_list), sum(frame_list)/len(frame_list)))