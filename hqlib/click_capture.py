import select


def click_capture(pipe, *, verbose=False):
    # import inside function to avoid errors if not using this module
    import evdev
    from evdev import ecodes, KeyEvent, event_factory

    # find the flirc device
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        if device.name.startswith("flirc.tv"):
            break
        device = None
    
    if device is None:
        raise ValueError("no flirc device found")

    print(f"found flirc: path: {device.path}, name: {device.name}, phys: {device.phys}")
    
    over = False
    for item in pipe:
        # wait for a click event...
        r, *_ = select.select([device], [], [], 1.0)
        if len(r) == 0:
            continue
        
        for event in device.read():
            if event.type != ecodes.EV_KEY:
                continue

            kev = event_factory[event.type](event)
            if verbose:
                print(kev)

            if kev.keystate != KeyEvent.key_up:
                continue

            if kev.scancode == ecodes.KEY_ENTER:
                yield item
            elif kev.scancode == ecodes.KEY_ESC:
                if kev.keystate == KeyEvent.key_up:
                    over = True
                    break
        
        if over:
            break



