# interface.py
import pyglet
from pyglet.window import key

class VideoDisplay:
    def __init__(self, width, height):
        self.window = pyglet.window.Window(width, height, caption='Video Display')
        self.window.set_location(200, 200)
        self.current_image = None
        self.window.on_draw = self.on_draw

    def process_frame(self, frame):
        # 假设 frame 是已经处理过的 NumPy 数组
        self.current_image = pyglet.image.ImageData(frame.shape[1], frame.shape[0],
                                                    'RGB', frame.tobytes(), pitch=-frame.shape[1]*3)
        self.window.flip()  # 更新窗口显示

    def on_draw(self):
        self.window.clear()
        if self.current_image:
            self.current_image.blit(0, 0)

    def run(self):
        pyglet.app.run()
