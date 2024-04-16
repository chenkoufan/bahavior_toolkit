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
        changed, checked =  imgui.checkbox("Active", self.active) # checked就是有没有选中
        if changed:
            self.active = checked
            if self.active:
                self.on_activated()
            else:
                self.on_deactivated()
    
    def on_activated(self):
        print("Filter activated")

    def on_deactivated(self):
        print("Filter deactivated")

    def frame_change(self, clip:KVideoNew):
        print("Video clip changed")
        pass

    def render(self, app:'KApp'):
        pass