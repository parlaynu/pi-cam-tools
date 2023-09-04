from pprint import pprint
import time
import os.path
from datetime import datetime

import piexif
import cv2
import numpy as np
from PIL import Image


def image_writer(input, odir, *, save_all=True):

    for idx, i in enumerate(input):
                
        camera_id, camera_mode = i['camera_id'], i['camera_mode']
        metadata = i['metadata']
            
        exif = _generate_exif(metadata, camera_id=camera_id)
        
        saved = []
        for k, image in i.items():
            if not isinstance(image, np.ndarray):
                continue

            # all the save methods expect 'RGB' not the 'BGR' of opencv
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

            # generate the image path prefix
            impath = os.path.join(odir, f"img-{idx:04d}-{k}")

            if k == 'raw':
                impath = _save_raw(impath, image, metadata=metadata, camera_mode=camera_mode)
                
            else:
                if save_all == False:
                    found = any(np.array_equal(image, i) for i in saved)
                    if found:
                        continue
                    
                impath = _save_jpg(impath, image, exif=exif)
                saved.append(image)
            
            newi = dict(i)
            newi['image_path'] = impath
            
            yield newi



def _generate_exif(metadata, *, camera_id=None):
    datetime_now = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    zero_ifd = {
        piexif.ImageIFD.Make: "Raspberry Pi",
        piexif.ImageIFD.Model: camera_id if isinstance(camera_id, str) else "unknown",
        piexif.ImageIFD.Software: "Picamera2",
        piexif.ImageIFD.DateTime: datetime_now
    }
    total_gain = metadata["AnalogueGain"] * metadata["DigitalGain"]
    exif_ifd = {
        piexif.ExifIFD.DateTimeOriginal: datetime_now,
        piexif.ExifIFD.ExposureTime: (metadata["ExposureTime"], 1000000),
        piexif.ExifIFD.ISOSpeedRatings: int(total_gain * 100)
    }
    exif = piexif.dump({"0th": zero_ifd, "Exif": exif_ifd})
    
    return exif

    
def _save_jpg(impath, image, *, quality=95, exif=None):
    impath += ".jpg"

    image = Image.fromarray(image)
    image.save(impath, quality=quality, exif=exif)
    
    return impath


def _save_png(impath, image, *, compress_level=6, exif=None):
    impath += ".png"
    
    image = Image.fromarray(image)
    image.save(impath, compress_level=compress_level, exif=exif)
    
    return impath


def _save_raw(impath, image, *, metadata, camera_mode):
    impath += ".dat"
    image.tofile(impath)
    
    return impath

