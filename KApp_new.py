
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

# read_file_path = 'data/test.mp4'
read_file_path = 'data/olin_original.MP4'
window_width = 900
window_height = 500
# scale_factor = 0.8
scale_factor = 0.36
cols = 40
rows = 20
start_x = 20
start_y = 20

class KGridPixel:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.rect : shapes.Rectangle = None
        self.data = {'R':0, 'G':0, 'B':0, 'A':0} # 用来存储每个矩形的数据,控制显示颜色等,这里是颜色的数据,可以改成其他数据
        self.active = False
        self.num = 0


class KApp:
    """
    window 管理gui,显示视频.处理输入
    filters 每个filter处理不用方面
    video 加载和处理视频文件
    current_video 正在编辑的视频片段
    """

    def __init__(self):
        super().__init__()
        self.batch = pyglet.graphics.Batch()
        self.window : KWindow = KWindow(window_width, window_height, self)
        self.filters : List[KFilter] = []
        self.video : KVideo = None
        self.current_video : KVideoNew = None
        self.current_filter_index = 0

        self.video_edit_start_time_sec = 0.0
        self.video_edit_end_time_sec = 1.0
        self.video_skip_frames = 5

        self.visual_threshold = 0.15
        self.visual_scale = 5.0

        self.frame_image = None
        self.video_height = None
        self.video_width = None

        self.frame_reading = 0
        self.update_timer = 0
        self.update_frequency = 2

        this_folder = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(this_folder, read_file_path)
        cap = cv2.VideoCapture(file_path) # 底图
        self.video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.cell_height = self.video_height*scale_factor / rows
        self.cell_width = self.video_width*scale_factor / cols
        #self.grid_xy = []

        self.grid : List[KGridPixel] = [] # 用来存储每个矩形(class)的数据,控制显示颜色等

        self.background = shapes.Rectangle(start_x, start_y, self.video_width*scale_factor, self.video_height*scale_factor, color=(0, 50, 150, 150)) # 底图
        self.background.draw()
        for row in range(rows):
            for col in range(cols):
                # 计算每个矩形的左下角坐标
                corner_x = start_x + col * self.cell_width
                corner_y = start_y + row * self.cell_height

                grid_pixel = KGridPixel(corner_x, corner_y)
                
                grid_pixel.rect = shapes.Rectangle(corner_x, corner_y, self.cell_width, self.cell_height, color=(0, 50, 150, 150), batch=self.batch) # 这里已经画了矩形了,相当于后面只用改它的颜色就行

                self.grid.append(grid_pixel)
        
        self.person_points = [] # 用来存储每个人点的位置

    def run(self):
        """调用KWindow的run(),启动pyglet主循环"""
        self.window.run() #KWindow content

    def update(self):
        self.update_timer += 1
        """调
        用一系列的 ImGui 界面创建方法来构建和管理 GUI
        
        """
        gl.glClearColor(0, 0.084, 0.255, 1)
        imgui.new_frame()

        imgui.begin("CustomFootprint")
        imgui.text(" Main Menu")

        if imgui.button("Load Video"):
            this_folder = os.path.dirname(os.path.abspath(__file__))
            file = os.path.join(this_folder, read_file_path) # 可加
            self.video = KVideo(file) # KVideo content 这里开始video变量进来, the video variable comes in

        #number input for start time
        #number input for end time

        changed, self.video_edit_start_time_sec =  imgui.input_float("Start Time", self.video_edit_start_time_sec)
        changed, self.video_edit_end_time_sec =  imgui.input_float("End Time", self.video_edit_end_time_sec)
        changed, self.video_skip_frames =  imgui.input_int("Skip Frames", self.video_skip_frames)

        if (imgui.button("Create Map")):
            self.current_video = self.video.get_video(self.video_edit_start_time_sec, self.video_edit_end_time_sec, self.video_skip_frames) # KVideoNew content, 从video中获取片段, get the clip from the video
            
            self.current_video.apply_yolo() # 新加的 current_video.tracker_data里就是yolo结果

        if (imgui.button("Reset")):
            self.reset()

        selection_changed, new_selection =  imgui.listbox("Filters", self.current_filter_index, [f.name for f in self.filters])

        if selection_changed:
            self.current_filter_index = new_selection # 选中的那个
        
        changed, self.visual_threshold = imgui.input_float("Threshold", self.visual_threshold)
        changed, self.visual_scale = imgui.input_float("Scale", self.visual_scale)
        self.filters[self.current_filter_index].update_ui(self) # 这里可以改frames内容,然后可视化,现在用了下面的方法分类,不过word_list用这个显示
        imgui.end()

        if self.current_video is not None : 
        # 就是filter里面的第二个
            self.data_visualisation()

        imgui.render()        
        
        # for f in self.filters:
        #     if f.active:
        #         f.render(self)

    def reset(self):
        for n in range(len(self.grid)):
            self.grid[n].data = {'R':0, 'G':0, 'B':0, 'A':0}
            self.grid[n].rect.color = (0, 50, 150, 150)
        self.frame_reading = 0
        self.background.draw()

    def advance_yolo_frame(self):
        
        if self.frame_reading < self.current_video.get_frame_count(): 
        # 利用update()来读取视频帧, read the video frame using update()              
            img = self.current_video.frames[self.frame_reading].frame_image # img是帧

            if self.frame_image is None:
                self.frame_image = pyglet.image.ImageData(img.shape[1], img.shape[0], 'BGR', img.tobytes())
            else:
                self.frame_image.set_data('BGR', -img.shape[1]*3, img.tobytes())

            self.last_img = img

        if self.frame_reading == self.current_video.get_frame_count():
        #读取完毕,显示最后一帧, read all the frames, show the last frame
            self.frame_image.set_data('BGR', -self.last_img.shape[1]*3, self.last_img.tobytes())

        # 上面就是更新底图内容,visualisation是显示内容
            
        if self.frame_reading < self.current_video.get_frame_count():
            # render the points detected in the current frame
            current_frame : KVideoFrame = self.current_video.frames[self.frame_reading]

            # use pyglet to draw the points
            self.person_points.clear()
            # for point in current_frame.mid_points:  # Show traces
            for i in range(len(current_frame.mid_points)): # 为了和clipdata对应i
                # Adjust xy-coordinate for Pyglet's coordinate system
                adjusted_x = current_frame.mid_points[i][0]*scale_factor + start_x
                adjusted_y = (self.video_height - current_frame.mid_points[i][1]) * scale_factor + start_x
                person_points = shapes.Circle(adjusted_x, adjusted_y, 3, color=(255, 0, 0),batch=self.batch)
                self.person_points.append(person_points) # 用来存储每个人点的位置,每次刷新都会清空,所以每次都要重新画

                dx = adjusted_x - start_x
                dy = adjusted_y - start_y
                colx = int(dx / self.cell_width)
                rowy = int(dy / self.cell_height)
                grid_num = rowy * cols + colx
                self.grid[grid_num].active = True
                self.grid[grid_num].num += 1

                if self.grid[grid_num].data['R'] < 255:
                #     self.grid[grid_num].data  += 50 # 这里相当于是最简单的cumulative sum
                    word0_data = current_frame.clip_datas['standing'][i] # 这里是clipdata的值
                    self.grid[grid_num].data['R'] += int(self.visual_scale * (float(word0_data)-self.visual_threshold)) # 这里是根据clipdata的值来改变颜色
                else:
                    self.grid[grid_num].data['R'] = 255

                if self.grid[grid_num].data['G'] < 255:
                #     self.grid[grid_num].data  += 50 # 这里相当于是最简单的cumulative sum
                    word1_data = current_frame.clip_datas['walking'][i] # 这里是clipdata的值
                    self.grid[grid_num].data['G'] += int(self.visual_scale * (float(word1_data)-self.visual_threshold)) # 这里是根据clipdata的值来改变颜色
                else:
                    self.grid[grid_num].data['G'] = 255            

                a_R = int(self.grid[grid_num].data['R']/self.grid[grid_num].num)
                a_G = int(self.grid[grid_num].data['G']/self.grid[grid_num].num)
                self.grid[grid_num].rect.color = (a_R, a_G, 0, 150) # 根据信息每次改颜色

        self.frame_reading += 1

    def advance_video_frame(self):
        self.person_points.clear()
        if self.frame_reading < self.current_video.get_frame_count(): 
        # 利用update()来读取视频帧, read the video frame using update()              
            img = self.current_video.frames[self.frame_reading].frame_image # img是帧

            if self.frame_image is None:
                self.frame_image = pyglet.image.ImageData(img.shape[1], img.shape[0], 'BGR', img.tobytes())
            else:
                self.frame_image.set_data('BGR', -img.shape[1]*3, img.tobytes())

            self.last_img = img

        if self.frame_reading == self.current_video.get_frame_count():
        #读取完毕,显示最后一帧, read all the frames, show the last frame
            self.frame_image.set_data('BGR', -self.last_img.shape[1]*3, self.last_img.tobytes()) 
        self.frame_reading += 1

    def data_visualisation(self:'KApp'):
        imgui.begin("Video Clip")
        imgui.text(f"Duration: {self.current_video.get_duration_sec()} sec")
        imgui.text(f"Frame Count: {self.current_video.get_frame_count()}")
        imgui.end()

        show_yolo = self.current_filter_index == 0
        show_video = self.current_filter_index == 1
        if self.update_timer % self.update_frequency == 0: # 30帧更新一次,但是更新的哪一帧还是前面的控制的
            # 统一在这里控制好了
            if show_yolo:
                self.advance_yolo_frame()
            elif show_video:
                self.advance_video_frame()

        if self.frame_image is not None: # 显示内容
            self.frame_image.blit(start_x, start_y, width=self.video_width*scale_factor, height=self.video_height*scale_factor)
            self.batch.draw()

if __name__ == '__main__':
    app = KApp()
    app.filters.append(KClipFilter())
    app.filters.append(KMotionPathsFilter())
    app.run()
    