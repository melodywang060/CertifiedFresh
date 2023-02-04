from PIL import Image
import numpy as np

im = Image.open('original_temp/small.png')

width, height = im.size   # Get dimensions

im_array = np.array(im)

new_width = width*0.8
new_height = height*0.8

left = (width - new_width)/2
top = (height - new_height)/2
right = (width + new_width)/2
bottom = (height + new_height)/2

# Crop the center of the image
im = im.crop((left, top, right, bottom))
im.save('cropped_images/original_ahhhh.jpg')