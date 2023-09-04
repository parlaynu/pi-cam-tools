# Pi HQCamera Utils

Some utilities for working with a Pi HQ Camera. They're pretty basic at the moment, but I've
found them useful.

The tools all work by creating a processing pipeline using python's generator functions and then
iterating over the output to activate the processing. It's a pretty simple way to put things 
together and I've found it easy to understand and extend.

Haven't tried them with the module 2 and 3 cameras.

The tools include:

|  Tool          | Description                                                   |
| -------------- | ------------------------------------------------------------- |
| cam-info.py    | displays some basic information about the camera capabilities |
| cam-preview.py | starts the camera with a preview output                       |
| cam-capture.py | captures a sequence of images to disk                         |
| cam-click.py   | uses a flirc usb receiver to trigger image captures           |
| cam-focus.py   | runs an autofocus algorithm from live camera or image files   |

## Setup

Install the necessary system packages:

    sudo apt install python3-pip python3-picamera2 python3-libcamera python3-opencv python3-numpy python3-pil

To use the `cam-click.py` utility, you will also need the `evdev` python package:

    pip3 install --user evdev

## General Utilities

### Camera Info

Displays the information about the camera available from the picamera2 library.

    ./cam-info.py

### Camera Preview

Simply creates and initialises the camera and starts a preview at HD resolution. 

Useful to make sure everything is connected and ready and is a chance to focus the camera.

    ./cam-preview.py

## Capture Utilities

### Camera Capture

Capture a sequence of still images from the camera. Options include the delay between successive captures,
the sensor mode to use (see `cam-info.py` for options), saving raw images as well as jpegs, and the
total number of images to capture.

    $ ./cam-capture.py -h
    usage: cam-capture.py [-h] [-p] [-m SENSOR_MODE] [-r] [-d DELAY] [-n NUM_IMAGES] outdir
    
    positional arguments:
      outdir                output directory to save images
      
    optional arguments:
      -h, --help            show this help message and exit
      -p, --preview         run the preview
      -m SENSOR_MODE, --sensor-mode SENSOR_MODE
                            the sensor mode for the camera (default: 10)
      -r, --capture-raw     capture raw images as well as the jpeg
      -d DELAY, --delay DELAY
                            delay in seconds between captures (default: 5)
      -n NUM_IMAGES, --num-images NUM_IMAGES
                            number of images to capture (default: 10)

An example run:

    $ ./cam-capture.py -n 6 -r -p images
    saved images/1693780889/img-0000-image.jpg
    saved images/1693780889/img-0000-raw.dat
    saved images/1693780889/img-0001-image.jpg
    saved images/1693780889/img-0001-raw.dat
    saved images/1693780889/img-0002-image.jpg
    saved images/1693780889/img-0002-raw.dat

### Click Capture

This uses a [flirc usb receiver](https://flirc.tv/products/flirc-usb-receiver?variant=43513067569384) to 
trigger captures. I've been using an old AppleTV remote as the controller.

Once you have configured the device to work with your remote control, plug it into the raspberry pi
and run the command and it should all work. Use the key you programmed as 'ENTER' to capture an
image and the key programmed as 'ESC' to quit the application.

The command takes the following form:

    $ ./cam-click.py -h
    usage: cam-click.py [-h] [-v] [-p] [-m SENSOR_MODE] [-r] outdir
    
    positional arguments:
      outdir                output directory to save images
      
    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         print remote control events
      -p, --preview         run the preview
      -m SENSOR_MODE, --sensor-mode SENSOR_MODE
                            the sensor mode for the camera (default: 10)
      -r, --capture-raw     capture raw images as well as the jpeg

An example run:

    $ ./cam-click.py -p images
    
    00 saved images/1693781264/img-0000-image.jpg
    01 saved images/1693781264/img-0001-image.jpg
    02 saved images/1693781264/img-0002-image.jpg

## Focus Utilities

### Camera Focus

Check the camera focus using a numeric algorithm. Start the application and then manually focus the
HQ camera to see the number varying. The higher the number, the sharper (better focussed) the image.

The actual value of the number will depend on the image contents - but the higher the better.

It only considers the region around the centre of the image which is, by default, 25% of the width and height,
but can be overridden on the command line.

Usage information is:

    $ ./cam-focus.py -h
      usage: cam-focus.py [-h] [-r ROI] [-s SMOOTH_ALG] [-f FOCUS_ALG] [imgdir]
      
      positional arguments:
        imgdir                directory to read images from (default: camera)
        
      optional arguments:
        -h, --help            show this help message and exit
        -r ROI, --roi ROI     centre percentage of image to use (default: 25)
        -s SMOOTH_ALG, --smooth-alg SMOOTH_ALG
                              the smoothing algorithm (default: hqlib.bilateral)
        -f FOCUS_ALG, --focus-alg FOCUS_ALG
                              the focus measure algorithm (default: hqlib.var_of_laplacian)

By default, images are read from the camera and smoothed with the smoothing algorithm, and a contrast or focus measure
calculated with the focus algorithm. There are a few available in the code - check the module to find them.

if an `imgdir` is specified, the images are read from disk.



