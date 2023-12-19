# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageChops
import sys
import numpy as np


image_1 = Image.open("../com_formate_logs/logs/images/20210331132134_a.png")
image_2 = Image.open("../com_formate_logs/logs/images/20210331132216_a.png")


diff = ImageChops.difference(image_1, image_2)
np_diff = np.array(diff)
#np.set_printoptions(threshold=sys.maxsize)

print("NumPy content: " + str(np_diff.shape))

# Count black pixels

black  = np.count_nonzero(np.all(np_diff))
print("Amount of black pixels:" + str(black))



diff.show(diff)
