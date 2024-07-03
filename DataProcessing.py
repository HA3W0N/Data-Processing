import sys
import cv2
import glob
import os
import random
import numpy as np

def Gaussian_Blur(img, sigma):
    result = cv2.GaussianBlur(img, (7,7), sigma)
    return result

def Downsampling(img, Factor):
    result = cv2.resize(img,(0 ,0), fx= Factor, fy=Factor)
    return result

def Resampling(img):
    result = cv2.resize(img, (224,224), interpolation= cv2.INTER_LINEAR)
    return result

def Additive_Noise(img, variance):
    std = np.sqrt(variance)
    noise = np.random.normal(0, std, img.shape)
    result = noise + img
    result = np.clip(result,0,255).astype(np.uint8)
    return result

def create_video(root, video_title, Original_fps, Corrupt_option):
    save_folder = os.path.join(root, video_title)
    output_path = os.path.join(root, f"{video_title}_{Corrupt_option}.mp4")
    
    # Get the list of image files in the save folder
    image_files = sorted(os.listdir(save_folder))

    # Create the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, Original_fps, (224, 224))
    
    # Write the frames to the video
    for image_file in image_files:
        image_path = os.path.join(save_folder, image_file)
        frame = cv2.imread(image_path)
        out.write(frame)
    
    out.release()

if __name__ == "__main__":
    metadata_file = "DataCorruption.txt"
    with open(metadata_file, "w")as f:
        f.write("Metadata of Data Corruption with Pixel-Downsample/Drop/Noise\n")
        f.write("\n File Name / Type / Frame Count / Corrupt Start / Corrupt End / Duration / Output File\n")
    # Use os.walk to traverse through all subfolders
    for root, dirs, files in os.walk('.'):
    # Use glob to filter only .mp4 files
        mp4_files = list(glob.glob(os.path.join(root, '*.mp4')))
        for videos in mp4_files:
            fps_list = [5, 10, 15, 20, 25]
            fps = random.choice(fps_list)
            count = 0

            print("MP4 Files : ", videos)

            video = cv2.VideoCapture(videos)
            Original_fps = video.get(cv2.CAP_PROP_FPS)
            video_title = os.path.splitext(os.path.basename(videos))[0]
            save_folder = os.path.join(root,video_title)
            os.makedirs(save_folder, exist_ok = True)

            seqstart = random.randint(1,video.get(cv2.CAP_PROP_FRAME_COUNT)) #SEQUENCE START # Subtract fps to save Minimum # Start with 1 Because of Identity
            #Example : 1 ~ 60
            seqend = seqstart + fps #SEQUENCE END
            randomfactor = (random.randint(10,20))/100 #DOWNSAMPLING FACTOR
            randomSigma = (random.randint(1,20))/10
            Noise_variance = 400

            #Probability
            prob = random.random()

            #Previous Image
            Previous = None

            #Corrupt option
            Corrupt_option = None
            while video.isOpened():
                ret, img = video.read()
                if ret:
                    if video.get(cv2.CAP_PROP_POS_FRAMES) > seqstart and video.get(cv2.CAP_PROP_POS_FRAMES) <= seqend:
                        #Image processing With Probability
                        # 0.2 Image Processing / 0.1 Frame Stop / 0.2 Gaussian Noise --> 0 - 0.2 Image Processing, 0.2 - 0.3 Frame Stop , 0.3 - 0.4 Gaussian Noise
                        if prob <= 0.2: 
                            img = Resampling(Downsampling(img, randomfactor))
                            Corrupt_option = "Downsample"

                        elif prob > 0.2 and prob <= 0.4:
                            img = Previous
                            Corrupt_option = "Freeze"
                        
                        elif prob > 0.4 and prob <= 0.6:
                            img = Additive_Noise(img, Noise_variance)
                            Corrupt_option = "GaussianNoise"
                        
                        elif prob > 0.6 and prob <= 0.8:
                            img = Gaussian_Blur(img, Noise_variance)
                            Corrupt_option = "GaussianBlur"

                        Previous = img
                        save_path = os.path.join(save_folder, f"{count:05d}.jpg")
                        cv2.imwrite(save_path, img)

                    else:
                        Corrupt_option = "None"
                        Previous = img
                        save_path = os.path.join(save_folder, f"{count:05d}.jpg")
                        cv2.imwrite(save_path, img)
                    count += 1
                else:
                    break
                    
            create_video(root, video_title, Original_fps, Corrupt_option)
            with open(metadata_file, "a") as f:
                f.write(" {} {} {} {} {} {} {} \n".format(videos,Corrupt_option,video.get(cv2.CAP_PROP_FRAME_COUNT),seqstart, seqend, fps, video_title+"_"+Corrupt_option+".mp4"))
            video.release()