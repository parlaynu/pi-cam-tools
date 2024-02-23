#!/usr/bin/env python3
import os
os.environ['LIBCAMERA_LOG_LEVELS'] = "*:WARN"

import time
import argparse
from itertools import islice

import hqlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--camera', help='the camera to query', type=int, default=0)
    parser.add_argument('-p', '--preview', help='run the preview', action='store_true')
    parser.add_argument('-m', '--sensor-mode', help='the sensor mode for the camera (default: 2)', type=int, default=2)
    parser.add_argument('-r', '--capture-raw', help='capture raw images as well as the jpeg', action='store_true')
    parser.add_argument('-d', '--delay', help='delay in seconds between captures (default: 5)', type=int, default=5)
    parser.add_argument('-n', '--num-images', help='number of images to capture (default: 10)', type=int, default=10)
    parser.add_argument('outdir', help='output directory to save images', type=str, default=None)
    args = parser.parse_args()

    # create the output directory
    capdir = os.path.join(args.outdir, str(int(time.time())))
    os.makedirs(capdir)

    # build the pipeline
    pipe = hqlib.camera(args.camera, mode=args.sensor_mode, preview=args.preview, capture_raw=args.capture_raw)
    pipe = hqlib.delay(pipe, value=args.delay)
    pipe = hqlib.image_writer(pipe, capdir)

    # and run...
    for i in islice(pipe, args.num_images):
        print(f"saved {i['image_path']}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
