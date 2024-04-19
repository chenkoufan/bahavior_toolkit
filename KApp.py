
from typing import List
import pyglet
from pyglet import gl
from pyglet import shapes
import imgui
from imgui.integrations.pyglet import create_renderer
import os
import cv2
import time

from KWindow import * # 管理窗口
from KVideo import * # 视频处理,包括导入完整视频,截取片段,视频内容处理(重点部分)
from KFilter import * # 
from KClipFilter import * # 
from KMotionPathFilter import *

class KApp:
    """
    window 管理gui,显示视频.处理输入
    filters 每个filter处理不用方面
    video 加载和处理视频文件
    current_video 正在编辑的视频片段

    """

    def __init__(self):
        super().__init__()
        self.window : KWindow = KWindow(1000, 500, self)
        self.filters : List[KFilter] = []
        self.video : KVideo = None
        self.current_video : KVideoNew = None
        self.current_filter_index = 0

        self.video_edit_start_time_sec = 0.0
        self.video_edit_end_time_sec = 1.0
        self.video_skip_frames = 5

        self.frame_image = None

        self.frame_reading = 0


    def run(self):
        """调用KWindow的run(),启动pyglet主循环"""
        self.window.run() #KWindow content

    def update(self):
        """调
        用一系列的 ImGui 界面创建方法来构建和管理 GUI
        
        """
        gl.glClearColor(0, 0.084, 0.255, 1)
        imgui.new_frame()

        imgui.begin("CustomFootprint")
        imgui.text(" Main Menu")

        if imgui.button("Load Video"):
            this_folder = os.path.dirname(os.path.abspath(__file__))
            file = os.path.join(this_folder, "data/test.mp4") # 可加
            self.video = KVideo(file) #KVideo content 这里开始video变量进来, the video variable comes in

        #number input for start time
        #number input for end time

        changed, self.video_edit_start_time_sec =  imgui.input_float("Start Time", self.video_edit_start_time_sec)
        changed, self.video_edit_end_time_sec =  imgui.input_float("End Time", self.video_edit_end_time_sec)
        changed, self.video_skip_frames =  imgui.input_int("Skip Frames", self.video_skip_frames)

        if (imgui.button("Create Map")):
            self.current_video = self.video.get_video(self.video_edit_start_time_sec, self.video_edit_end_time_sec, self.video_skip_frames) # KVideoNew content, 从video中获取片段, get the clip from the video
            # for f in self.filters: # KFilter content,还没操作, not operated yet, 批量生成的时候用,现在先一个个来
            #     f.on_video_clip_changed(self.current_video) 
            #     # 就是加一层滤镜,不同滤镜代表不同的处理内容,现在是pass

            # self.filters[self.current_filter_index].frame_change() # 因为要逐帧换,所以后来在update()里面处理

        selection_changed, new_selection =  imgui.listbox("Filters", self.current_filter_index, [f.name for f in self.filters])

        if selection_changed:
            self.current_filter_index = new_selection # 选中的那个

        self.filters[self.current_filter_index].update_ui(self) # 这里可以改frames内容,然后可视化

        imgui.end()

        if self.current_video is not None:
            imgui.begin("Video Clip")
            imgui.text(f"Duration: {self.current_video.get_duration_sec()} sec")
            imgui.text(f"Frame Count: {self.current_video.get_frame_count()}")
            imgui.end()
            
            if self.frame_reading < self.current_video.get_frame_count(): 
            # 利用update()来读取视频帧, read the video frame using update()

                img = self.current_video.frames[self.frame_reading].frame_image # img是帧
                img = self.filters[self.current_filter_index].frame_change(img) # 变换frame
                
                # 准备显示第一帧, prepare to show the first frame, ????why can't use .get_frame[0]????
                if self.frame_image is None:
                    self.frame_image = pyglet.image.ImageData(img.shape[1], img.shape[0], 'BGR', img.tobytes())
                else:
                    self.frame_image.set_data('BGR', -img.shape[1]*3, img.tobytes())

                self.frame_image.blit(20, 20, width=640, height=400)

                self.frame_reading += 1
                time.sleep(1/30)
                self.last_img = img
            

            if self.frame_reading == self.current_video.get_frame_count():
            #读取完毕,显示最后一帧, read all the frames, show the last frame
                self.frame_image.set_data('BGR', -self.last_img.shape[1]*3, self.last_img.tobytes())
                self.frame_image.blit(20, 20, width=640, height=400)
        
        for f in self.filters:
            if f.active:
                f.render(self)

        imgui.render()
        

if __name__ == '__main__':
    app = KApp()
    app.filters.append(KClipFilter())
    app.filters.append(KMotionPathsFilter())
    app.run()
    