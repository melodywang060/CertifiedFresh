import argparse
import imutils
import cv2
import numpy as np
from PIL import Image

img = cv2.imread('images/tomato-plant.jpg')

# threshold red
lower = np.array([0, 0, 0])
upper = np.array([40, 50, 255])
thresh = cv2.inRange(img, lower, upper)
    
# Change non-red to white
result = img.copy()
result[thresh != 255] = (255,255,255)

cv2.imwrite('color_temp/result.jpg', result)


