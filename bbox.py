import argparse
import imutils
import cv2
import numpy

# load image
# display image
image = cv2.imread("color_temp/result.jpg")
cv2.imshow("Image", image)
baseimage = image.copy()
#cv2.waitKey(0)

# to grayscale :D
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray", gray)
cv2.imwrite("bbox_temp/index_gray.png", gray)
#cv2.waitKey(0)

# blurring
blur = cv2.GaussianBlur(gray, (5,5), 0)
cv2.imshow("Blur", blur)
cv2.imwrite("bbox_temp/index_blur.png", blur)
#cv2.waitKey(0)

# creating a threshold image
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imwrite("temp/index_thresh.png", thresh)

# create kernals + dilation
kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (3,10))
cv2.imwrite("bbox_temp/index_kernal.png", kernal)

dilate = cv2.dilate(thresh, kernal, iterations=1)
cv2.imwrite("bbox_temp/index_dilate.png", dilate)

# create contours
contours = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1] # what
contours = sorted(contours, key = lambda x: cv2.boundingRect(x)[0])

original_img = cv2.imread("resized_images/banana.jpg")

letter = ''

for c in contours:
	x, y, w, h = cv2.boundingRect(c)
	if w*h > 100000:
		print(w*h)
		cv2.rectangle(original_img, (x, y), (x+w, y+h), (36, 255, 12), 2)
		rect = cv2.minAreaRect(c)
		box = cv2.boxPoints(rect)
		box = numpy.int0(box)
		# cv2.drawContours(original_img, [box], 0, (0,0,255), 2)
		cv2.imwrite("bbox_temp/out.png", original_img)
		
		small = original_img[y:y+h, x:x+w]
		cv2.imwrite("bbox_temp/small.png", small)

cv2.imwrite("bbox_temp/index_bbox.png", original_img)




# eliminate contours that are too small!

