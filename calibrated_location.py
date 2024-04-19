import cv2
import numpy as np

def calibrated_location(image_path, point_A, new_width, new_height):
    img = cv2.imread(image_path)
    # cv2.imshow('Original Image', img)

    # 手动定义四个角点和点A
    points = [(841, 607), (1370, 600), (1637, 866), (544, 845)]

    # 显示这些点
    for pt in points:
        cv2.circle(img, pt, 5, (0, 255, 0), -1)
    cv2.circle(img, point_A, 5, (0, 0, 255), -1)
    cv2.imshow('Points Marked', img)

    # 透视变换
    src_pts = np.array(points, dtype="float32")
    dst_pts = np.array([[0, 0], [new_width, 0], [new_width, new_height], [0, new_height]], dtype="float32")
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    transformed_img = cv2.warpPerspective(img, M, (new_width, new_height))
    
    # 变换点A
    point_A_transformed = cv2.perspectiveTransform(np.array([[point_A]], dtype="float32"), M)
    transformed_x, transformed_y = point_A_transformed[0][0] # 变换后坐标
    cv2.circle(transformed_img, (int(transformed_x), int(transformed_y)), 5, (0, 0, 255), -1)

    # 显示变换后的图像和点A
    cv2.imshow('Transformed Image', transformed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return transformed_x, transformed_y

if __name__ == "__main__":
    point_A = (1122, 723)
    calibrated_location('data/test.png',point_A, 300, 400)
