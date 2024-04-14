from KFilter import *

class KMotionPathsFilter(KFilter):
    def __init__(self):
        super().__init__()
        self.name = "Motion Paths Filter"

    def update_ui(self, app:'KApp'):
        super().update_ui(app)

    def render(self, app:'KApp'):
        super().render(app)

    def on_video_clip_changed(self, clip:KVideoClip):
        super().on_video_clip_changed(clip)
        