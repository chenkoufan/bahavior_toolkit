import os
import cv2

from yolo_detect import yolo_process_frame
from interfaceTest import VideoDisplay

video_path = os.path.join('.', 'data', 'test.MP4')
video_out_path = os.path.join('.','outcome', 'test.mp4')
# crop_image_path = 'outcome/crop_scale'

cap = cv2.VideoCapture(video_path) # 打开视频文件
ret, frame = cap.read() # 读取第一帧

display = VideoDisplay(1560,800)

cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'MP4V'), cap.get(cv2.CAP_PROP_FPS),
                          (frame.shape[1], frame.shape[0])) # 初始化VideoWriter,用于保存视频

frame_interval = 10
frame_count = 0



# words = ['summer', 'autumn','spring', 'winter','T-shirts','cardigan','sweater','blazer','windbreaker','overcoat','dress','shorts','leggings','trousers','jeans']
words = ['summer', 'autumn', 'spring','winter']


while ret:
    ret, frame = cap.read()
    if not ret:
        break  # 如果没有帧了，退出循环

    if frame_count % frame_interval != 0: # 帧间隔
        frame_count += 1
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    tracker = yolo_process_frame(frame, words,frame_count)
    display.update_frame(frame)     

    # cap_out.write(frame) # 保存视频    
    # cv2.imshow('Real-time Preview', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # 如果按下ESC则退出 这样停一下才可以保证preview
        break

    frame_count += 1
    
display.close()
cap.release()
cap_out.release()
cv2.destroyAllWindows()



