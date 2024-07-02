import sys
import cv2
import glob
import os
import DataCorruption as dc

# image_path
# video_name

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
                        if int(video.get(1) % (video.get(cv2.CAP_PROP_FPS) / fps))==0:
                            save_path = os.path.join(save_folder, f"{count:05d}.jpg")
                            cv2.imwrite(save_path, img)
                            count += 1
                    else:
                        break
                video.release()
