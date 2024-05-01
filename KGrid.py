import numpy as np
from pyglet import shapes
from Kcolor_normalize import *
from pyglet.text import Label


class KGridPixel:
    cols = 40
    rows = 20
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.rect : shapes.Rectangle = None
        self.color_data = np.array([0.0,0.0,0.0,0.0]) # 用来存储每个矩形的数据,控制显示颜色等,这里是颜色的数据,可以改成其他数据
        self.active = False
        self.num = 0

    @property
    def RGBAtuple(self):
        return colorTuple(self.color_data[0], self.color_data[1], self.color_data[2], self.color_data[3])
    

    def getData(self, use_mean):
        if use_mean and self.num>0:
            return self.color_data/self.num
        return self.color_data


class AGridPixel(KGridPixel):
    cols = 8
    rows = 6
    def __init__(self, x:int, y:int, frame_x:int, frame_y:int, frame_width:int, frame_height:int):
        super().__init__(x,y)
        
        self.frame_x = frame_x
        self.frame_y = frame_y
        self.frame_width = frame_width
        self.frame_height = frame_height
        

        self.clip_data = {}
        self.label = Label('',
                           font_name='Times New Roman',
                           font_size=6,
                           x=self.x, y=self.y,
                           anchor_x='left', anchor_y='bottom')
        
    def crop_image(self, frame:np.ndarray):
        return frame[int(self.frame_y):int(self.frame_y+self.frame_height), int(self.frame_x):int(self.frame_x+self.frame_width)]