
from KFilter import *
import numpy as np
from KVideo import *
# from yolo_detect_frame import yolo_process_frame # basic visualisation
 

class KClipFilter(KFilter):
    def __init__(self):
        super().__init__()
        self.words :List[str] = ["cat"]
        self.name = "Clip Filter"

    def update_ui(self, app:'KApp'):
        super().update_ui(app)
        if imgui.button("Add Word"):
            self.words.append("new word")
        for i, word in enumerate(self.words):
            imgui.push_id(str(i))
            changed, new_word = imgui.input_text("", word, 256)
            if changed:
                self.words[i] = new_word
            imgui.pop_id()
        
    def frame_change(self, frame : np.ndarray , increase_value=50):        
        # yolo_process_frame(frame)
        print("Video clip changed")
        return frame
    
    def frame_change2(self, frame : KVideoFrame, increase_value=50):        
        yolo_process_frame2(frame)
        print("Video clip changed")
        return frame
        

    def render(self, app:'KApp'):
        super().render(app)
        # if app.current_video is None:
        #     return
        # cframe = app.current_video.frames[app.frame_reading]
        
        # tracker = cframe.tracker_data

        #draw the points on the image 