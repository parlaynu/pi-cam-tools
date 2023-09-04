import os
import cv2


def image_reader(idir, *, recurse=False, sort=False):

    images = os.scandir(idir)
    if sort:
        images = list(images)
        images.sort(key=lambda x: x.name)

    for entry in images:
        if entry.is_dir() and recurse:
            yield from image_reader(entry.path, recurse=recurse, sort=sort)
        
        elif entry.is_file():
            im = cv2.imread(entry.path, cv2.IMREAD_COLOR)
            
            i = {
                'orig': im,
                'image':im,
                'image_path': entry.path
            }
            yield i
