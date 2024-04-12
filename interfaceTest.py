# interface.py
import cv2
import pyglet
from pyglet.window import key

class VideoDisplay:
    def __init__(self, video_path):
        self.width, self.height = 1560, 800
        self.window = pyglet.window.Window(self.width, self.height, caption='Video Display')
        self.window.set_location(200, 200)

        # 使用 OpenCV 加载视频
        self.cap = cv2.VideoCapture(video_path)

        # 全局变量来存储当前帧的图像数据
        self.current_image = None

        # 绑定事件处理方法
        self.window.on_draw = self.on_draw
        self.window.on_key_press = self.on_key_press

        # 每次更新画面的时间间隔
        pyglet.clock.schedule_interval(self.update, 1/30.0)  # 设置为视频的帧率

    def update(self, dt):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_image = pyglet.image.ImageData(frame.shape[1], frame.shape[0],
                                                        'RGB', frame.tobytes(), pitch=-frame.shape[1]*3)

    def on_draw(self):
        self.window.clear()
        if self.current_image:
            display_width = 640
            display_height = 400
            self.current_image.blit(50, self.height - display_height - 50, width=display_width, height=display_height)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.Q or symbol == key.ESCAPE:
            pyglet.app.exit()

    def run(self):
        pyglet.app.run()

    def close(self):
        self.cap.release()
