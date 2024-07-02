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

                seqstart = random.randint(1,video.get(cv2.CAP_PROP_FRAME_COUNT)) #SEQUENCE START # Subtract fps to save Minimum # Start with 1 Because of Identity
                #Example : 0 ~ 60-fps , if fps 5  Extract between 0 ~ 55 
                seqend = seqstart + fps #SEQUENCE END
                randomfactor = (random.randint(10,20))/100 #DOWNSAMPLING FACTOR

                #Probability
                prob = (random.randint(0,100))/100

                #Previous Image
                Previous = None
                
                #Record Metadata
                metadata_file = os.path.join(save_folder, "{}_{}.txt".format(video_title, fps))
                with open(metadata_file, "a") as f:
                    f.write("Sequence Start : {} , Sequence End : {}, Random Factor of DownSampling : {} ".format(seqstart, seqend, randomfactor))
                    if prob > 0.3:
                        f.write("\nThere is No Image Processing or DROP")
                
                while video.isOpened():
                    ret, img = video.read()
                    if ret:
                        if video.get(cv2.CAP_PROP_POS_FRAMES) > seqstart and video.get(cv2.CAP_PROP_POS_FRAMES) <= seqend:
                            #Image processing With Probability
                            # 0.2 Image Processing / 0.1 Frame Stop
                            if prob <= 0.2: 
                                img = Resampling(Downsampling(img, randomfactor))
                                with open(metadata_file, "a") as f: 
                                    f.write("\nDownsampling Frame Number : {} ".format(count))
                            elif prob > 0.2 and prob <= 0.3:
                                img = Previous
                                with open(metadata_file, "a") as f:
                                    f.write("\nStop Frame : {} ".format(count))

                                    
                            Previous = img
                            save_path = os.path.join(save_folder, f"{count:05d}.jpg")
                            cv2.imwrite(save_path, img)

                        else:
                            Previous = img
                            save_path = os.path.join(save_folder, f"{count:05d}.jpg")
                            cv2.imwrite(save_path, img)
                        count += 1
                    else:
                        break

                video.release()