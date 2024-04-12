import cv2


def clip_visualize(words, tracker,id, frame, x1, y1, x2, y2):
    content = ''
    # words = ['summer', 'autumn', 'spring','winter']
    # top_consider = ['T-shirts','cardigan','sweater','blazer','windbreaker','overcoat']
    # bottom_consider = ['dress','shorts','leggings','trousers','jeans']
    
    # 找到对应值最大的键
    season_max = max(words, key=lambda k: tracker.clip_datas[id][k])

    cv2.putText(frame, str(id), (int(x1), int(y1)), 0, 5e-3 * 150, (255, 0, 0), 2)
    cv2.putText(frame, season_max, (int(x2), int(y1)), 0, 5e-3 * 150, (255, 0, 0), 2)    

    cv2.putText(frame, str(tracker.exist_time[id]), (int(x2), int(y1+60)), 0, 5e-3 * 150, (0, 0, 255), 2)
