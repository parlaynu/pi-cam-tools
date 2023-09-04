import cv2
import numpy as np


def var_of_laplacian(input):
    
    for i in input:
        im = i['smooth']
        
        im = cv2.Laplacian(im, cv2.CV_64F)
        i['laplacian'] = im
        
        i['focus'] = im.var()
        
        yield i


def canny_edges(input):
    
    for i in input:
        im = i['smooth']
        
        im = cv2.Canny(im, 0, 30, apertureSize=3)
        i['canny'] = im
        
        i['focus'] = float(np.count_nonzero(im)) / float(im.shape[0] * im.shape[1])
        
        yield i


