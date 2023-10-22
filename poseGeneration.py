import os
import cv2
import numpy as np
from PIL import Image
from moviepy.editor import *
import copy
import gradio as gr
from transformers import AutoTokenizer, CLIPTextModel
from huggingface_hub import snapshot_download
import sys
import argparse

sys.path.append('FollowYourPose')

def get_frames(video_in):
    frames = []
    #resize the video
    clip = VideoFileClip(video_in)
    start_frame = 0
    end_frame = int(clip.fps * clip.duration)


    if not os.path.exists('./raw_frames'):
        os.makedirs('./raw_frames')

    if not os.path.exists('./mmpose_frames'):
        os.makedirs('./mmpose_frames')

    #check fps
    if clip.fps > 30:
        print("vide rate is over 30, resetting to 30")
        clip_resized = clip.resize(height=512)
        clip_resized = clip_resized.subclip(start_frame / clip_resized.fps, end_frame / clip_resized.fps) # subclip 2 seconds
        clip_resized.write_videofile("./video_resized.mp4", fps=30)
        end_frame = int(30 * clip_resized.duration)
    else:
        print("video rate is OK")
        clip_resized = clip.resize(height=512)
        clip_resized = clip_resized.subclip(start_frame / clip.fps, end_frame / clip.fps) # subclip 5 seconds
        clip_resized.write_videofile("./video_resized.mp4", fps=clip.fps)
        end_frame = int(clip.fps * clip_resized.duration)

    print("video resized to 512 height")

    # Opens the Video file with CV2
    cap= cv2.VideoCapture("./video_resized.mp4")

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print("video fps: " + str(fps))
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite('./raw_frames/kang'+str(i)+'.jpg',frame)
        frames.append('./raw_frames/kang'+str(i)+'.jpg')
        i+=1

    cap.release()
    cv2.destroyAllWindows()
    print("broke the video into frames")

    return frames, fps

def get_mmpose_filter(mmpose, i):
    #image = Image.open(i)

    #image = np.array(image)
    image = mmpose(i, fn_index=0)[1]
    image = Image.open(image)
    #image = Image.fromarray(image)
    image.save("./mmpose_frames/mmpose_frame_" + str(i).split('/')[-1][:-4] + ".jpeg")
    return "./mmpose_frames/mmpose_frame_" + str(i).split('/')[-1][:-4] + ".jpeg"

def create_video(frames, fps, video_type, output_directory="/content/ict3104-team17-2023/pose_input"):
    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    print("building video result")
    clip = ImageSequenceClip(frames, fps=fps)
    output_filename = f"{video_type}_result.mp4"
    output_path = os.path.join(output_directory, output_filename)
    clip.write_videofile(output_path, fps=fps)
    
    return output_path


def infer_skeleton(mmpose, video_in):


    # 1. break video into frames and get FPS

    break_vid = get_frames(video_in)
    frames_list= break_vid[0]
    fps = break_vid[1]
    #n_frame = int(trim_value*fps)
    n_frame = len(frames_list)

    if n_frame >= len(frames_list):
        print("video is shorter than the cut value")
        n_frame = len(frames_list)

    # 2. prepare frames result arrays
    result_frames = []
    print("set stop frames to: " + str(n_frame))

    for i in frames_list[0:int(n_frame)]:
        mmpose_frame = get_mmpose_filter(mmpose, i)
        result_frames.append(mmpose_frame)
        print("frame " + i + "/" + str(n_frame) + ": done;")


    final_vid = create_video(result_frames, fps, "mmpose")
    files = [final_vid]

    return final_vid, files

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Infer Skeleton from Video")
    parser.add_argument("input_video", help="Path to the input video file")
    args = parser.parse_args()
    
    mmpose = gr.Interface.load(name="spaces/YueMafighting/mmpose-estimation")
    final_vid, files = infer_skeleton(mmpose, args.input_video)
