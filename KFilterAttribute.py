
from KFilter import *
import numpy as np
from KVideo import *
# from yolo_detect_frame import yolo_process_frame # basic visualisation
 

class KFilterClipAttribute(KFilter):
    def __init__(self):
        super().__init__()
        self.words :List[str] = ["cat"]
        self.name = "Clip Attribute Filter"
        

    def update_ui(self, app: 'KApp'):
        super().update_ui(app)

        if imgui.button("Add Word"):
            self.words.append("new word")  # 添加新词

        # 为每个单词创建一个输入框和删除按钮
        for i in range(len(self.words)):
            imgui.push_id(str(i))
            changed, new_word = imgui.input_text("", self.words[i], 256)
            if changed:
                self.words[i] = new_word  # 更新单词

            # 添加删除按钮，每个单词旁边
            if imgui.button("Delete"):
                self.words.pop(i)  # 删除当前索引的单词
                imgui.pop_id()  # 确保及时跳出当前循环避免迭代问题
                break  # 防止迭代器失效，退出循环

            imgui.pop_id()  # 弹出ID，确保每个元素有唯一ID
        
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