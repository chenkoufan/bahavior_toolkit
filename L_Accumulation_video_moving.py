import cv2
import numpy as np

# 视频文件路径
video_file = 'data/test.mp4'
# 输出视频路径
output_video_file = 'city_video/accumulation/output_video.mp4'

transparency = 0.01  # 透明度

cap = cv2.VideoCapture(video_file)

ret, last_frame = cap.read()
if not ret:
    print("Failed to read the video.")
    cap.release()
    exit()

height, width = last_frame.shape[:2]

# 初始化VideoWriter对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_fps = cap.get(cv2.CAP_PROP_FPS)  # 使用原视频的帧率
out = cv2.VideoWriter(output_video_file, fourcc, output_fps, (width, height))

motion_accumulated_frame = np.zeros((height, width), np.float32)

while True:
    ret, current_frame = cap.read()
    if not ret:
        break

    frame_diff = cv2.absdiff(current_frame, last_frame)
    gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)

    # 使用一个标量而不是数组来调整灰度差异的强度
    scaled_gray_diff = cv2.multiply(gray_diff, transparency)  # 直接使用标量进行乘法

    _, motion_mask = cv2.threshold(scaled_gray_diff, 0, 255, cv2.THRESH_BINARY)
    transparent_motion = cv2.min(scaled_gray_diff, motion_mask)

    # 使用透明度更新motion_accumulated_frame
    np.add(motion_accumulated_frame, transparent_motion, out=motion_accumulated_frame, casting="unsafe")
    motion_accumulated_frame = np.clip(motion_accumulated_frame, 0, 255)

    motion_accumulated_8bit = cv2.convertScaleAbs(motion_accumulated_frame)

    # 写入处理后的帧到输出视频
    out.write(motion_accumulated_8bit)

    last_frame = current_frame

    # 显示结果
    cv2.imshow('Motion Accumulation', motion_accumulated_8bit)

    if cv2.waitKey(1) & 0xFF == 27:  # 按Esc键退出
        break

# 释放资源
cap.release()
out.release()  # 释放VideoWriter对象
cv2.destroyAllWindows()
