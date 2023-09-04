
def roi(input, percent):
    
    for i in input:
        im = i['image']
        
        ishape = im.shape
        
        ysize = int(ishape[0] * percent / 100)
        ystart = int((ishape[0] - ysize)/2)

        xsize = int(ishape[1] * percent / 100)
        xstart = int((ishape[1] - xsize)/2)
        
        i['image'] = im[ystart:ystart+ysize, xstart:xstart+xsize, :]
        
        yield i

