import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image


## 이미지 크롭 함수
# pil_img : Image.open()으로 가져온 이미지<br>
# step_x : 잘라낼 가로 시작점<br>
# step_y : 잘라낼 세로 시작점<br>
# width : 잘라낼 가로 크기<br>
# height : 잘라낼 세로 크기<br>

# In[2]:

def cropImage(pil_img, step_x, step_y, width, height):

    area = (step_x, step_y, width, height)
    crop_img = pil_img.crop(area)

    return crop_img