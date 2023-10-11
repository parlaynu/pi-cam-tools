#!/usr/bin/env python3
import argparse
import time
from pprint import pprint

import hqlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help='the display mode', type=int, default=1)
    parser.add_argument('-v', '--video', help='video use case', action='store_true')
    parser.add_argument('--vflip', help='flip the image vertically', action='store_true')
    parser.add_argument('--hflip', help='flip the image horizontally', action='store_true')
    args = parser.parse_args()

    pipe = hqlib.camera(
        preview=True, 
        mode=args.mode, 
        video=args.video, 
        vflip=args.vflip,
        hflip=args.hflip
    )
    
    for i in pipe:
        time.sleep(15)
        pprint(i['metadata'])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

