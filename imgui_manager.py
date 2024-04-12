# words_manager.py
import imgui
from imgui.integrations.pyglet import PygletRenderer
import pyglet

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

