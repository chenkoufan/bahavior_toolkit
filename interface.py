# interface.py
import pyglet
from pyglet.window import key
import imgui
from imgui.integrations.pyglet import PygletRenderer

class VideoDisplay:
    def __init__(self, width=1560, height=800):
        self.width = width
        self.height = height
        self.window = pyglet.window.Window(self.width, self.height, caption='Video Display')
        self.window.set_location(200, 200)

        # 全局变量来存储当前帧的图像数据
        self.current_image = None

        # 绑定事件处理方法
        self.window.on_draw = self.on_draw
        self.window.on_key_press = self.on_key_press

        # 不再需要自己加载视频和设置更新间隔
        # pyglet.clock.schedule_interval(self.update, 1/30.0)

    def update_frame(self, frame):
        """ 更新当前帧图像数据 """
        if frame is not None:
            # 假设 frame 已经是 RGB 格式
            self.current_image = pyglet.image.ImageData(frame.shape[1], frame.shape[0],
                                                        'RGB', frame.tobytes(), pitch=-frame.shape[1]*3)
            # 手动调用重绘窗口
            self.window.dispatch_events()
            self.window.dispatch_event('on_draw')
            self.window.flip()

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
        pass  # 由外部控制资源释放


class WordsManager:
    def __init__(self):
        # Initialize Pyglet window
        self.window = pyglet.window.Window(width=800, height=600, caption='Word Editor')
        imgui.create_context()
        self.renderer = PygletRenderer(self.window)

        # Initialize the words list
        self.words = ['example', 'initial', 'words']

        # Event handlers
        self.window.on_draw = self.on_draw

    def run(self):
        pyglet.app.run()

    def on_draw(self):
        # Clear the window and setup new imgui frame
        self.window.clear()
        imgui.new_frame()

        # Draw the imgui window
        if imgui.begin("Words Editor"):
            # List each word with an option to edit and delete
            idx_to_delete = -1
            for idx, word in enumerate(self.words):
                imgui.push_id(str(idx))  # Convert index to string
                _, new_word = imgui.input_text("", word, 256)
                if imgui.is_item_deactivated_after_edit() and new_word.strip():
                    self.words[idx] = new_word.strip()
                    print(self.words)  # Print updated words list
                if imgui.button("delete"):
                    idx_to_delete = idx
                imgui.pop_id()
                imgui.separator()

            # Add a button to append new words
            if imgui.button("Add New Word"):
                self.words.append("new word")
                print(self.words)  # Print updated words list

            if idx_to_delete >= 0:
                self.words.pop(idx_to_delete)
                print(self.words)  # Print updated words list

            imgui.end()

        # Render the imgui onto the screen
        imgui.render()
        self.renderer.render(imgui.get_draw_data())


    def close(self):
        # Shutdown imgui and renderer properly
        self.renderer.shutdown()
        self.window.close()

if __name__ == '__main__':
    manager = WordsManager()
    try:
        manager.run()
    finally:
        manager.close()

