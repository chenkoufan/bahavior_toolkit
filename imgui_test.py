import pygame
import imgui
from imgui.integrations.pygame import PygameRenderer

def main():
    pygame.init()
    size = 800, 600
    screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)

    imgui.create_context()
    renderer = PygameRenderer()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            renderer.process_event(event)

        

        # 更新DisplaySize为当前窗口大小
        width, height = screen.get_size()
        imgui.get_io().display_size = width, height

        imgui.new_frame()

        # 这里添加你的ImGui绘制代码
        # 创建一个简单的窗口
        if imgui.begin("Demo Window"):
            imgui.text("Hello, ImGui!")
            if imgui.button("Click Me"):
                print("Button Clicked")
            imgui.end()

        imgui.render()
        renderer.render(imgui.get_draw_data())
        pygame.display.flip()

if __name__ == "__main__":
    main()
