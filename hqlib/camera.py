from pprint import pprint

from picamera2 import Picamera2, Preview
from libcamera import Transform, controls


def camera(camid, *, mode=2, video=False, preview=False, capture_raw=False, vflip=False, hflip=False):

    print(f"running with sensor mode {mode}")

    cam = Picamera2(camid)
    # for idx, sensor_mode in enumerate(cam.sensor_modes):
    #     print(f"sensor mode {idx}:")
    #     pprint(sensor_mode)
    
    sensor_mode = cam.sensor_modes[mode]
    raw_format = sensor_mode['unpacked']
    raw_size = sensor_mode['size']
    
    main_size = raw_size

    # take special care with size if we're previewing
    preview_size = None
    if preview:
        preview_size = (1920, 1080)
        if main_size[0] < preview_size[0] or main_size[1] < preview_size[1]:
            main_size = preview_size

    kwargs = {
        # 'buffer_count': 2,
        # 'controls': {
        #     'FrameDurationLimits': (33333, 500000),
        # },
        'main': {
            'size': main_size,
            'format': 'RGB888'
        },
        'queue': False
    }
    
    if capture_raw:
        kwargs['raw'] = {
            'size': raw_size,
            'format': str(raw_format)
        }
        
    if preview:
        kwargs['lores'] = {
            'size': preview_size
        }
        kwargs['display'] = 'lores'

    if vflip or hflip:
        kwargs['transform'] = Transform(vflip=vflip, hflip=hflip)
    
    if video:
        config = cam.create_video_configuration(**kwargs)
    else:
        config = cam.create_still_configuration(**kwargs)

    cam.align_configuration(config)
    cam.configure(config)
    
    print("camera properties:")
    pprint(cam.camera_properties)
    
    print("camera controls:")
    pprint(cam.camera_controls)

    print("camera config:")
    pprint(cam.camera_config)
    
    # set some controls
    # cam.set_controls({
    #     "AwbMode": controls.AwbModeEnum.Daylight,
    # })
        
    if preview:
        cam.start_preview(Preview.DRM, width=1920, height=1080)
    cam.start()
    
    arrays = ['main']
    if capture_raw:
        arrays.append('raw')
    
    while True:
        # capture the image and metadata
        images, metadata = cam.capture_arrays(arrays)
        
        i = {
            'camera_id': cam.camera.id,
            'camera_mode': mode,
            'image':images[0],
            'metadata': metadata
        }

        if capture_raw:
            i['raw'] = images[1]
        
        yield i
