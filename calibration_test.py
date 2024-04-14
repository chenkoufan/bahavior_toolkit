import cv2
import numpy as np

# 全局变量存储点和状态
points = []
point_A = None

def click_event(event, x, y, flags, params):
    global point_A
    # 鼠标左键点击事件
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append((x, y))
            cv2.circle(img, (x, y), 5, (0, 255, 0), -1)  # 用绿色标记前四个点
        elif len(points) == 4:
            point_A = (x, y)
            points.append(point_A)
            cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # 用红色标记第五个点，即点A
        cv2.imshow('image', img)

def main(image_path):
    global img
    img = cv2.imread(image_path)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)

    # 等待点的选择
    while True:
        cv2.imshow('image', img)
        if cv2.waitKey(20) & 0xFF == 27 or len(points) == 5:
            break

    if len(points) == 5:
        # 透视变换
        src_pts = np.array(points[:4], dtype="float32")
        dst_pts = np.array([[0, 0], [300, 0], [300, 300], [0, 300]], dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        dst = cv2.warpPerspective(img, M, (300, 300))

        # 显示变换后的图像
        cv2.imshow('Transformed', dst)

        # 变换点A
        point_A_transformed = cv2.perspectiveTransform(np.array([[point_A]], dtype="float32"), M)
        transformed_x, transformed_y = point_A_transformed[0][0]
        cv2.circle(dst, (int(transformed_x), int(transformed_y)), 5, (0, 0, 255), -1)
        cv2.imshow('Transformed with Point A', dst)

        cv2.waitKey(0)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main('data/test.png')
