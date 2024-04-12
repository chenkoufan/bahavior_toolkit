# main.py
from interfaceTest import VideoDisplay

if __name__ == "__main__":
    video_path = 'data/olin_large.MP4'  # 确保更换为你的视频路径
    video_display = VideoDisplay(video_path)
    video_display.run()
    video_display.close()
