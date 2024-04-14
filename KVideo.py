from typing import List
import os
import cv2


class KYoloData:
    def __init__(self):
        super().__init__()
        self.class_name = ''
        self.confidence = 0.0
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

class KVideoFrame:
    def __init__(self):
        super().__init__()
        self.time_stamp_sec = 0.0
        self.image = None

        self.yolo_data : List[KYoloData]  = []


class KVideoClip:
    def __init__(self):
        super().__init__()
        self.start_time_sec = 0.0
        self.end_time_sec = 0.0
        self.frames : List[KVideoFrame] = []

    def add_frame(self, frame:KVideoFrame):
        self.frames.append(frame)

    def get_frame(self, index:int):
        return self.frames[index]

    def get_frame_count(self):
        return len(self.frames)

    def get_duration_sec(self):
        return self.end_time_sec - self.start_time_sec

    def get_frame_index(self, time_sec:float):
        pass

class KVideo:
    def __init__(self, file:str):
        super().__init__()
        self.file = file
        self.duration_sec = 0.

    def get_clip(self, start_time_sec:float, end_time_sec:float, skip_frames:int=0) -> KVideoClip:
        
        clip = KVideoClip()
        clip.start_time_sec = start_time_sec
        clip.end_time_sec = end_time_sec

        #open video file
        cap = cv2.VideoCapture(self.file)
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time_sec * 1000)
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % skip_frames == 0:
                video_frame = KVideoFrame()
                video_frame.image = frame
                video_frame.time_stamp_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                clip.add_frame(video_frame)
            frame_count += 1
            if video_frame.time_stamp_sec >= end_time_sec:
                break

        cap.release()


        return clip