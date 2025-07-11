import cv2
import bisect
import random
import os
from tqdm import tqdm

class DatasetCreator:
    def __init__(self, dataset_size):
        self.dataset_size = dataset_size
        self.VIDEOS_PATH = "Dataset Videos"
        self.OUTPUT_DIR = "Dataset"
    
    def create_dataset(self):
        video_paths = []
        video_frames = []
        boundaries = []

        directory = os.path.join(os.getcwd(), self.VIDEOS_PATH)
        for filename in tqdm(os.listdir(directory), desc="Listing video files"):
            video_path = os.path.join(directory, filename)
            video_paths.append(video_path)

        if video_paths:
            for video_path in tqdm(video_paths, desc="Getting frame counts"):
                cap = cv2.VideoCapture(video_path)
                frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                video_frames.append(frames)
                cap.release()

            boundaries.append(0)
            for i in tqdm(range(len(video_frames)), desc="Building boundaries"):
                boundaries.append(boundaries[-1] + video_frames[i])

            global_frames = random.sample(range(sum(video_frames)), self.dataset_size)

            for frame in tqdm(global_frames, desc="Extracting frames"):
                index = bisect.bisect_right(boundaries, frame) - 1
                local_frame = frame - boundaries[index]
                try:
                    cap = cv2.VideoCapture(video_paths[index])
                    cap.set(cv2.CAP_PROP_POS_FRAMES, local_frame)
                    ret, image = cap.read()
                    cap.release()
                    if ret:
                        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
                        cv2.imwrite(f"{self.OUTPUT_DIR}/frame_{frame}.jpg", image)
                    else:
                        print(f"Failed to read frame {frame}")
                except Exception as e:
                    print("CAP PROP FRAME COUNT ERROR, PROCEED")