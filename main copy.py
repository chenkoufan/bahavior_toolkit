import os
import random
import time
import cv2

from ultralytics import YOLO
from tracker import Tracker

from clipImage_function import clip_image
from clip_visualization import clip_visualize

video_path = os.path.join('.', 'data', 'franny426.MP4')
video_out_path = os.path.join('.','outcome', 'test.mp4')
# crop_image_path = 'outcome/crop_scale'

cap = cv2.VideoCapture(video_path) # 打开视频文件
ret, frame = cap.read() # 读取第一帧

cap_out = cv2.VideoWriter(video_out_path, cv2.VideoWriter_fourcc(*'MP4V'), cap.get(cv2.CAP_PROP_FPS),
                          (frame.shape[1], frame.shape[0])) # 初始化VideoWriter,用于保存视频

frame_interval = 10
frame_count = 0

model = YOLO("yolov8n.pt")
tracker = Tracker()
colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for j in range(10)]
detection_threshold = 0.5 # 可能性0.5以上的算作人
person_class_id = 0 # 人的id,做分类,其实好像是除了视频路径外的唯一的东西

mid_points = [] # 储存每人的位置点
mid_points_color = []

rec_crop = []
# words = ['summer', 'autumn','spring', 'winter','T-shirts','cardigan','sweater','blazer','windbreaker','overcoat','dress','shorts','leggings','trousers','jeans']
words = ['summer', 'autumn', 'spring','winter']
clip_datas = {}


while ret:
    ret, frame = cap.read()
    if not ret:
        break  # 如果没有帧了，退出循环

    if frame_count % frame_interval != 0: # 帧间隔
        frame_count += 1
        continue

    results = model(frame) # 获取YOLO模型的输出

    for result in results: # 用while每帧都有输出,results是一个list,里面是每个检测到的物体result
        detections = []
        for r in result.boxes.data.tolist(): 
            x1, y1, x2, y2, score, class_id = r # id is in classlist
            if score > detection_threshold and class_id == person_class_id:
                x1 = int(x1)
                x2 = int(x2)
                y1 = int(y1)
                y2 = int(y2)
                class_id = int(class_id)             
                detections.append([x1, y1, x2, y2, score])
        tracker.update(frame, detections) # 更新tracker,这样就可以跟踪人了
        
        for track in tracker.tracks: # tracker.tracks->list of Track 针对每个人
            bbox = track.bbox
            x1, y1, x2, y2 = bbox
            dy = y2 - y1
            dx = x2 - x1
            ratio = dy/dx
            body_correction = ratio > 2 and ratio < 5
            track_id = track.track_id # 保证每个track都有一个id,这个id是唯一的,所以可以跟踪人,获取他的id,然后画框
            
            if body_correction: # 因为每次都是tracker中更新,所以干脆弄个字典好了
                if not track_id in tracker.clip_datas: # 第一次录入,初始化
                    tracker.first_time[track_id] = frame_count // 30 # 初始化时间
                    # tracker.clip_datas[track_id] = {} # 初始化id对应的一系列数据

                #截取出画面
                crop_frame = frame[int(y1):int(y2), int(x1):int(x2)]
                
                # 保存截取的图片
                # crop_filename = os.path.join(crop_image_path, f"{track_id}.jpg")
                # cv2.imwrite(crop_filename, crop_frame)
                # rec_crop.append(track_id) # 记录是否crop过了,后来决定每次都算clip

                tracker.last_time[track_id] = frame_count // 30 # 对应帧的时间
                tracker.exist_time[track_id] = tracker.last_time[track_id] - tracker.first_time[track_id] # 计算待的时间
                
                clip_data = clip_image(words,crop_frame) # 对这个人clip计算 words-value                
                # tracker.clip_datas[track_id] = clip_data # 储存数据,这样相当于每次都更新了数据,改为列表         
                
                # for word in words:
                #     if not word in tracker.clip_datas[track_id]:
                #         tracker.clip_datas[track_id][word] = [] # 初始化                
                
                # for key in clip_data:
                #     tracker.clip_datas[track_id][key].append(clip_data[key]) # 更新数据,可以体现过程,而不是只有最后的结果,但是可视化时候不用这个,可以只用clip_data,但这个有必要吗

                tracker.clip_datas[track_id] = clip_data # 更新数据,可以体现过程,而不是只有最后的结果,但是可视化时候不用这个,可以只用clip_data,但这个有必要吗

            if body_correction: # visualization
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (colors[track_id % len(colors)]), 3) # 画框
                # cv2.putText(frame, str(track_id)+str(clip_data), (int(x1), int(y1)), 0, 5e-3 * 150, (255, 0, 0), 2) # 显示dict内容
                clip_visualize(words, tracker,track_id, frame, x1, y1, x2, y2)         
            
            mid_point = (int((x1 + x2) / 2), int(y2))
            tracker.mid_points_color.append(colors[track_id % len(colors)])
            tracker.mid_points.append(mid_point)               
          
    for i in range(1, len(mid_points)): # show traces
        cv2.circle(frame, tracker.mid_points[i], 3, tracker.mid_points_color[i], -1)

    # cap_out.write(frame) # 保存视频
    cv2.imshow('Real-time Preview', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # 如果按下ESC则退出 这样停一下才可以保证preview
        break

    frame_count += 1

cap.release()
cap_out.release()
cv2.destroyAllWindows()



