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
        self.frame_image = None

        # self.yolo_data : List[KYoloData]  = [] # 之后可以用来存储yolo数据, store yolo data


class KVideoNew:
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

    def get_video(self, start_time_sec:float, end_time_sec:float, skip_frames:int=0) -> KVideoNew: # 用这个得到截取片段
        
        new_video = KVideoNew() # 用来储存片段, get the new video
        new_video.start_time_sec = start_time_sec
        new_video.end_time_sec = end_time_sec

        #open video file
        cap = cv2.VideoCapture(self.file)
        cap.set(cv2.CAP_PROP_POS_MSEC, start_time_sec * 1000) # 设置开始时间, set the start time
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % skip_frames == 0:
                video_frame = KVideoFrame()
                video_frame.frame_image = frame # frame储存到KVideoframe.image里, store the frame in KVideoframe.image
                video_frame.time_stamp_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                new_video.add_frame(video_frame)
            frame_count += 1
            if video_frame.time_stamp_sec >= end_time_sec:
                break

        cap.release()

        return new_video # 是一个类,然后self.frames里面有很多frames,这些frame是用Class KVideoFrame储存的