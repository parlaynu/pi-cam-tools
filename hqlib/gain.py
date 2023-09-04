import cv2
import numpy as np


def autogain(input, key='image'):
    
    for i in input:
        im = i[key]
        
        mn, mx = im.min(), im.max()
        
        scale = 255 / mx
        
        im = im * scale

        i[key] = im.astype(np.uint8)
        
        yield i
