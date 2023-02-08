import numpy as np
from patchify import patchify

from PIL import Image

image = Image.open('bbox_temp/small.png')
image = np.asarray(image)

