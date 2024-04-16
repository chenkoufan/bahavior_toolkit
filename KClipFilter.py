
from KFilter import *
import numpy as np

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
        
    def frame_change(self,frame, increase_value=50):
        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Convert to float32 for more precision for modifications
        hsv_image = hsv_image.astype(np.float32)

        # Increase the saturation value
        hsv_image[:, :, 1] = hsv_image[:, :, 1] + increase_value
        # Ensure that the saturation values don't go beyond 255
        hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1], 0, 255)

        # Convert back to uint8 from float32
        hsv_image = hsv_image.astype(np.uint8)

        # Convert the HSV image back to BGR color space
        bgr_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
        print("Video clip changed")
        return bgr_image
        
        pass
        

    def render(self, app:'KApp'):
        super().render(app)