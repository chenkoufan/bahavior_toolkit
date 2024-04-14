

from typing import List
import pyglet
from pyglet import gl
from pyglet import shapes
import imgui
from imgui.integrations.pyglet import create_renderer
import os

from KVideo import *


class KFilter:    
    def __init__(self):
        super().__init__()
        self.name = ''
        self.active = True

    def update_ui(self, app:'KApp'):
        imgui.text(self.name)
        changed, checked =  imgui.checkbox("Active", self.active)
        if changed:
            self.active = checked
            if self.active:
                self.on_activated()
            else:
                self.on_deactivated()
    
    def on_activated(self):
        print(f"{self.name} activated")

    def on_deactivated(self):
        print(f"{self.name} deactivated")

    def on_video_clip_changed(self, clip:KVideoClip):
        pass

    def render(self, app:'KApp'):
        pass