import sys
import glob
import cv2
import os


def create_video(root, video_title, fps_list, Original_fps):
    for fps in fps_list:
        fps_rate = str(fps)
        save_folder = os.path.join(root, video_title, fps_rate)
        output_path = os.path.join(root, video_title, f"{video_title}_{fps_rate}.mp4")
        
        # Get the list of image files in the save folder
        image_files = sorted(os.listdir(save_folder))
        print(image_files)
        
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
    for root, dirs, files in os.walk('.'):
        mp4_files = list(glob.glob(os.path.join(root, '*.mp4')))
        for videos in mp4_files:
            video_title = os.path.splitext(os.path.basename(videos))[0]
            fps_list = [5, 10, 15, 20, 25]
            try:
                video = cv2.VideoCapture(videos)
                Original_fps = video.get(cv2.CAP_PROP_FPS)
                create_video(root, video_title, fps_list, Original_fps)
            except FileNotFoundError:
                print("Skip : {} Because the file doesn't exist from the beginning".format(video_title))
                continue
