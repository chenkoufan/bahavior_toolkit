import cv2
import numpy as np

# Global variables
points_map = []

def click_event_map(event, x, y, flags, params):
    global points_map, map_img
    if event == cv2.EVENT_LBUTTONDOWN and len(points_map) < 4:
        points_map.append((x, y))
        cv2.circle(map_img, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('Map Image', map_img)

def main(image_path, map_image_path):
    global img, map_img
    img = cv2.imread(image_path)
    map_img = cv2.imread(map_image_path)

    h, w = img.shape[:2]
    points = [(0, 0), (w - 1, 0), (w - 1, h - 1), (0, h - 1)]

    for point in points:
        cv2.circle(img, point, 5, (0, 255, 0), -1)
    cv2.imshow('Image', img)

    cv2.imshow('Map Image', map_img)
    cv2.setMouseCallback('Map Image', click_event_map)

    while len(points_map) < 4:
        if cv2.waitKey(20) & 0xFF == 27:
            break

    if len(points_map) == 4:
        src_pts = np.array(points, dtype="float32")
        dst_pts = np.array(points_map, dtype="float32")
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        transformed_image = cv2.warpPerspective(img, M, (map_img.shape[1], map_img.shape[0]))

        # 使用addWeighted叠加原图和变换后的图像到map_img上
        overlay = cv2.addWeighted(map_img, 1, transformed_image, 0.7, 0)
        cv2.imshow('Overlay Comparison', overlay)
        cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main('data/test.png', 'data/map.png')
