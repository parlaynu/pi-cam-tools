import cv2


def gaussian(input):
    
    for i in input:
        im = i['image']
        
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.GaussianBlur(im, ksize=(7,7), sigmaX=1.5, sigmaY=1.5)
        
        i['smooth'] = im
        
        yield i


def bilateral(input):
    
    for idx, i in enumerate(input):
        im = i['image']
        
        # d = 2*idx + 1
        d = 9
        
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.bilateralFilter(im, d=d, sigmaColor=2*d, sigmaSpace=d)
        
        i['smooth'] = im
        
        yield i


def nlmeans(input):
    
    for i in input:
        im = i['image']
        
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = cv2.fastNlMeansDenoising(im)
        
        i['smooth'] = im
        
        yield i
