import sys
import cv2
import glob
import os
import random

def Downsampling(img, Factor):
    result = cv2.resize(img,(0 ,0), fx= Factor, fy=Factor)
    return result

def Resampling(img):
    result = cv2.resize(img, (224,224), interpolation= cv2.INTER_LINEAR)
    return result

if __name__ == "__main__":
    # Use os.walk to traverse through all subfolders
    for root, dirs, files in os.walk('.'):
    # Use glob to filter only .mp4 files
        mp4_files = list(glob.glob(os.path.join(root, '*.mp4')))
        print(mp4_files)
        for videos in mp4_files:
            fps_list = [5, 10, 15, 20, 25]
            for fps in fps_list:
                count = 0
                print("roots : ", root)
                print("MP4 Files : ", videos)
                video = cv2.VideoCapture(videos)
                video_title = os.path.splitext(os.path.basename(videos))[0]
                fps_rate = str(fps)
                save_folder = os.path.join(root,video_title,fps_rate)
                os.makedirs(save_folder, exist_ok = True)
                while video.isOpened():
                    ret, img = video.read()
                    if ret:
                        randomfactor = (random.randint(0,50))/100
                        if int(video.get(1) % (video.get(cv2.CAP_PROP_FPS) / fps))==0:
                            #Image processing With Probability
                            if randomfactor <=0.2 and randomfactor >= 0.1:
                                img = Resampling(Downsampling(img, randomfactor))
                            
                            save_path = os.path.join(save_folder, f"{count:05d}.jpg")
                            cv2.imwrite(save_path, img)
                        else:
                            save_path = os.path.join(save_folder, f"{count:05d}.jpg")
                            cv2.imwrite(save_path, img)
                        count += 1

                    else:
                        break

                video.release()
