import os
import cv2
import numpy as np
import pandas as pd
from natsort import natsorted
from HelperCLIP import ClipHelper  # 确保HelperCLIP库是可用的，并提供了所需的功能

# 定义词汇和图片文件夹路径
# words = ['spring', 'summer', 'autumn', 'winter','T-shirts', 'sweater','coat','shorts','skirt','trousers',]
# words = ['hat','hatted','unhatted','no hat']
# words = ['scarf',]
# words = ['leather shoes','brogues','Derbies ','sneakers','boots','loafer','sandals',]
# words = ['Happy','Sad','Angry','Excited','Depressed','Fearful','Content','Nervous','Relieved',]
# words = ['gloved','ungloved','hands inside','hands outside']
# words = ['T-shirt','hoodie', 'sweater','coat']
# words = ['spring', 'summer', 'autumn', 'winter','T-shirts', 'sweater','coat','shorts','skirt','trousers','derbies','sneakers','boots','sandals']
clip_model = ClipHelper()

def clip_image(words, image):
    # 创建ClipHelper实例
    

    # 对每个词汇生成向量
    word_vectors = [clip_model.encodeText(w) for w in words]

    # 读取指定的图片
    # image = cv2.imread(image_path) # 导进的相当于已经读取了,为了方便一起放下面了
    # img_vec = clip_model.encodeImage(image)
    img_vec = clip_model.encodeImage(image)

    # 创建存储相似度的字典
    similarity_dict = {}

    # 计算每个词汇与图片的相似度并保存到字典中
    for i, word in enumerate(words):
        sim = np.dot(img_vec.flatten(), word_vectors[i].flatten())
        similarity_dict[word] = f"{sim:.3f}"

    # # 初始化相似度字典，每个键对应的值是空列表
    # similarity_dict = {word: [] for word in words}
    # # 计算每个词汇与图片的相似度并保存到字典中
    # for i, word in enumerate(words):
    #     sim = np.dot(img_vec.flatten(), word_vectors[i].flatten())
    #     # 将相似度得分添加到对应词汇的列表中
    #     similarity_dict[word].append(f"{sim:.3f}")

    # 返回相似度字典
    return similarity_dict

if __name__ == '__main__':
    # 示例使用
    words = ['spring', 'summer', 'autumn', 'winter']
    image_path = 'myimages/crop_scale/2.jpg'
    frame = cv2.imread(image_path)
    x1, y1, x2, y2 = 0, 0, 50, 50
    crop_frame = frame[int(y1):int(y2), int(x1):int(x2)]

    result = clip_image(words, crop_frame)
    print(result)