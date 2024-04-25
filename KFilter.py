from typing import List
import pyglet
from pyglet import gl
from pyglet import shapes
import imgui
from imgui.integrations.pyglet import create_renderer
import os

from KVideo import *


class KFilter:
    rows = 20
    cols = 40
    def __init__(self):
        super().__init__()
        self.name = ''
        self.active = True
        self.filters = ['accu','mean']
        self.accu_mean = 0


    def update_ui(self, app:'KApp'):
        imgui.text(self.name)
        changed, checked =  imgui.checkbox("Active", self.active) # checked就是有没有选中
        if changed:
            self.active = checked
            if self.active:
                self.on_activated()
            else:
                self.on_deactivated()

        # 加计算平均和总数值的选项
        selection_changed, new_selection =  imgui.listbox("vis_data", self.accu_mean, [f for f in self.filters])
        if selection_changed:
            self.accu_mean = new_selection # 选中的那个
    
    def on_activated(self):
        print("Filter activated")

    def on_deactivated(self):
        print("Filter deactivated")

    def frame_change(self, clip:KVideoNew):
        print("Video clip changed")
        pass

    def render(self, app:'KApp'):
        pass