from KFilter import *
from KApp_new import KGridPixel

#todo
class KFilterFrequency(KFilter):
    def __init__(self):
        super().__init__()
        self.name = "Show Frequency"

    def update_ui(self, app:'KApp'):
        super().update_ui(app)

    def frame_change(self):
        print("Video clip changed")
        pass

    def render(self, app:'KApp'):
        super().render(app)

    def on_video_clip_changed(self, clip:KVideoNew):
        super().on_video_clip_changed(clip)
        