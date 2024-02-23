import cv2
import numpy as np


def autogain(input, key='image'):

    orig_key = f"orig_{key}"
    for i in input:
        im = i[orig_key] = i[key]
        
        mn, mx = im.min(), im.max()
        
        scale = 255 / mx
        
        im = im * scale

        i[key] = im.astype(np.uint8)
        
        yield i
