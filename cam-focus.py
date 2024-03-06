#!/usr/bin/env python3
import argparse
import importlib

import hqlib


def create_callable(name):
    callable_path = name.split('.')
    callable_name = callable_path[-1]
    callable_module_path = '.'.join(callable_path[0:-1])
    
    callable_module = importlib.import_module(callable_module_path)
    callable_fn = getattr(callable_module, callable_name)

    return callable_fn


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--camera', help='the camera to query', type=int, default=0)
    parser.add_argument('-r', '--roi', help='centre percentage of image to use (default: 25)', type=int, default=25)
    parser.add_argument('-s', '--smooth-alg', help='the smoothing algorithm (default: hqlib.bilateral)', type=str, default="hqlib.bilateral")
    parser.add_argument('-f', '--focus-alg', help='the focus measure algorithm (default: hqlib.var_of_laplacian)', type=str, default="hqlib.var_of_laplacian")
    parser.add_argument('imgdir', help='directory to read images from (default: camera)', type=str, nargs='?', default=None)
    args = parser.parse_args()

    # build the pipeline
    
    if args.imgdir is None:
        pipe = hqlib.camera(args.camera, preview=True)
    else:
        pipe = hqlib.image_reader(args.imgdir, recurse=True, sort=True)
    
    pipe = hqlib.roi(pipe, args.roi)
    
    pipe = create_callable(args.smooth_alg)(pipe)
    pipe = create_callable(args.focus_alg)(pipe)
    
    print(f"focus check alg: {args.focus_alg}")
    print(f"  smoothing alg: {args.smooth_alg}")

    # and run...
    for idx, i in enumerate(pipe):
        imgpath = i.get('image_path', None)
        if imgpath is None:
            print(f"focus: {i['focus']}")
        else:
            print(f"focus: {imgpath}: {i['focus']}")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
