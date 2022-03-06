import cv2
import math
import numpy as np

def perspective_warp(image, transform):
  h, w = image.shape[:2]
  corners_bef = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)
  corners_aft = cv2.perspectiveTransform(corners_bef, transform)
  xmin = math.floor(corners_aft[:, 0, 0].min())
  ymin = math.floor(corners_aft[:, 0, 1].min())
  xmax = math.ceil(corners_aft[:, 0, 0].max())
  ymax = math.ceil(corners_aft[:, 0, 1].max())
  x_adj = math.floor(xmin - corners_aft[0, 0, 0])
  y_adj = math.floor(ymin - corners_aft[0, 0, 1])
  translate = np.eye(3)
  translate[0, 2] = -xmin
  translate[1, 2] = -ymin
  corrected_transform = np.matmul(translate, transform)
  return cv2.warpPerspective(image, corrected_transform, (math.ceil(xmax - xmin), math.ceil(ymax - ymin))), x_adj, y_adj

img = cv2.imread("img2.jpg")
T = np.eye(3)

rot = np.zeros((2, 2))
alpha = math.pi/4

rot[0][0] = math.cos(alpha)
rot[1][1] = math.cos(alpha)
rot[0][1] = -math.sin(alpha)
rot[1][0] = math.sin(alpha)

rot *= 2 

transl = np.zeros((2))
transl[0] = 400
transl[1] = -100

T[0:2, 0:2] = rot
T[0:2, 2] = transl

print(T)

# img, _, _ = perspective_warp(img, T)
img = cv2.warpPerspective(img, T, (img.shape[0] + 100, img.shape[1] + 100))

cv2.imshow("", img)
key = cv2.waitKey(10000)


