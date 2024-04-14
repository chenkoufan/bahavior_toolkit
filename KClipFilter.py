
from KFilter import *

class KClipFilter(KFilter):
    def __init__(self):
        super().__init__()
        self.words :List[str] = ["cat"]
        self.name = "Clip Filter"

    def update_ui(self, app:'KApp'):
        super().update_ui(app)
        if imgui.button("Add Word"):
            self.words.append("new word")
        for i, word in enumerate(self.words):
            imgui.push_id(str(i))
            changed, new_word = imgui.input_text("", word, 256)
            if changed:
                self.words[i] = new_word
            imgui.pop_id()
        

    def render(self, app:'KApp'):
        super().render(app)