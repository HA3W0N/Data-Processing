import sys
import cv2
import glob
import os
import random
import numpy as np
import ffmpeg
from scipy.io import wavfile


if __name__ == "__main__":
    audio_frame_list=[]
    metadata_file = 'Audio_Inpainting.txt'
    with open(metadata_file, "w") as f:
        f.write("Metadata of Audio Drop\n")
        f.write("\n File Name / Sampling Rate / Frame Count / Drop Start / Drop End / Drop Length / Output File \n")
    # Use os.walk to traverse through all subfolders
    for root, dirs, files in os.walk('.'):
    # Use glob to filter only .mp4 files
        mp4_files = list(glob.glob(os.path.join(root, '*.mp4')))
        for videos in mp4_files:
            #mp4 TO wav 
            video_title = os.path.splitext(os.path.basename(videos))[0]
            save_folder = os.path.join(root,video_title)
            print("MP4 Files : ", videos)
            input_file = videos
            output_file = save_folder + '.wav'
            print("Convert {} to {}".format(input_file, output_file))
            stream = ffmpeg.input(input_file)
            stream = ffmpeg.output(stream, output_file)
            ffmpeg.run(stream, overwrite_output=True)

            #Audio Inpainting
            fs, data = wavfile.read(output_file)
            # print("Sampling Rate : ", fs)
            # print("Total Frame : ", data.shape)
            # print("Frame : ", data)
            audio_frame_list.append(data.shape[0])
            random_length = [0, 80, 160, 240, 320] #Hz 
            length = random.choice(random_length)
            if length in [80, 160, 240, 320]:
                frame_length = 20 * length
                seqstart = random.randint(1,data.shape[0])
                seqend = seqstart + frame_length
                # print("Seq start : {}, Seq end : {}".format(seqstart, seqend))

                data[seqstart:seqend] = 0
                processingaudio = save_folder + '_drop.wav'
                wavfile.write(processingaudio, fs, data.astype(np.int16))

                with open(metadata_file, 'a') as f:
                    f.write(" {} {} {} {} {} {} {} \n".format(output_file, fs, data.shape[0], seqstart, seqend, frame_length, processingaudio))
            else:
                processingaudio = save_folder + '_none.wav'
                wavfile.write(processingaudio, fs, data.astype(np.int16))
                with open(metadata_file, 'a') as f:
                    f.write(" {} {} {} {} {} {} {} \n".format(output_file, fs, data.shape[0], "None", "None", "None", processingaudio))

            print("Finish. There is {} wav files, Maximum frame : {}, Minimum frame : {} , Mean : {} ".format(len(audio_frame_list), max(audio_frame_list), min(audio_frame_list), sum(audio_frame_list)/len(audio_frame_list)))




    