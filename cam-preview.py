#!/usr/bin/env python3
import argparse
import time
from pprint import pprint

import hqlib


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--camera', help='the camera to query', type=int, default=0)
    parser.add_argument('-m', '--mode', help='the display mode', type=int, default=7)
    parser.add_argument('-v', '--video', help='video use case', action='store_true')
    parser.add_argument('--vflip', help='flip the image vertically', action='store_true')
    parser.add_argument('--hflip', help='flip the image horizontally', action='store_true')
    args = parser.parse_args()

    pipe = hqlib.camera(
        args.camera,
        preview=True, 
        mode=args.mode, 
        video=args.video, 
        vflip=args.vflip,
        hflip=args.hflip
    )
    
    for idx, i in enumerate(pipe):
        print("--------------------------")
        metadata = i['metadata']
        for key in sorted(metadata.keys()):
            if key == "PispStatsOutput" or key == "Bcm2835StatsOutput":
                continue
            print(f"{key}: {metadata[key]}")
        time.sleep(2)




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

