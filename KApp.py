
from typing import List
import pyglet
from pyglet import gl
from pyglet import shapes
import imgui
from imgui.integrations.pyglet import create_renderer
import os
import cv2

from KWindow import *
from KVideo import *
from KFilter import *
from KClipFilter import *
from KMotionPathFilter import *

class KApp:

    def __init__(self):
        super().__init__()
        self.window : KWindow = KWindow(1000, 800, self)
        self.filters : List[KFilter] = []
        self.video : KVideo = None
        self.current_clip : KVideoClip = None
        self.current_filter_index = 0

        self.video_edit_start_time_sec = 0.0
        self.video_edit_end_time_sec = 0.0
        self.video_skip_frames = 5

        self.frame_image = None


    def run(self):
        self.window.run()




    def update(self):
        gl.glClearColor(1, 0, 0, 1)
        imgui.new_frame()


        imgui.begin("main")
        imgui.text("Hello, world!")

        if imgui.button("Load Video"):
            this_folder = os.path.dirname(os.path.abspath(__file__))
            file = os.path.join(this_folder, "data/test.mp4")
            self.video = KVideo(file)

        #number input for start time
        #number input for end time

        changed, self.video_edit_start_time_sec =  imgui.input_float("Start Time", self.video_edit_start_time_sec)
        changed, self.video_edit_end_time_sec =  imgui.input_float("End Time", self.video_edit_end_time_sec)
        changed, self.video_skip_frames =  imgui.input_int("Skip Frames", self.video_skip_frames)


        if (imgui.button("Create Clip")):
            self.current_clip = self.video.get_clip(self.video_edit_start_time_sec, self.video_edit_end_time_sec, self.video_skip_frames)
            for f in self.filters:
                f.on_video_clip_changed(self.current_clip)


        selection_changed, new_selection =  imgui.listbox("Filters", self.current_filter_index, [f.name for f in self.filters])

        if selection_changed:
            self.current_filter_index = new_selection

        self.filters[self.current_filter_index].update_ui(self)

        imgui.end()

        if self.current_clip is not None:
            imgui.begin("Video Clip")
            imgui.text(f"Duration: {self.current_clip.get_duration_sec()} sec")
            imgui.text(f"Frame Count: {self.current_clip.get_frame_count()}")
            imgui.end()

            img = self.current_clip.frames[0].image
            if self.frame_image is None:
                self.frame_image = pyglet.image.ImageData(img.shape[1], img.shape[0], 'BGR', img.tobytes())
            else:
                self.frame_image.set_data('BGR', -img.shape[1]*3, img.tobytes())

            self.frame_image.blit(0, 0, width=640, height=400)
        
        for f in self.filters:
            if f.active:
                f.render(self)

        imgui.render()

        

if __name__ == '__main__':
    app = KApp()
    app.filters.append(KClipFilter())
    app.filters.append(KMotionPathsFilter())
    app.run()