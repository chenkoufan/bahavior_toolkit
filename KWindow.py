
from typing import List
import pyglet
from pyglet import gl
from pyglet import shapes
import imgui
from imgui.integrations.pyglet import create_renderer
import os
import cv2

class KWindow(pyglet.window.Window):
    def __init__(self, width:int, height:int, app:'KApp'):
       #config = pyglet.gl.Config(double_buffer=True)
        #config = pyglet.gl.Config(sample_buffers=1, samples=0)
        super().__init__(width=width, height=height)#, config=config)

        imgui.create_context()
        self.imguiImpl = create_renderer(self)
        self.app = app

    def on_draw(self):
        self.clear() 
        self.app.update() # spp is KApp, clear and update
        self.imguiImpl.render(imgui.get_draw_data())
        #self.flip()

    def run(self):
        pyglet.app.run()