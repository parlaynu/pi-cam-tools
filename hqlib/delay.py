import time


def delay(pipe, *, value=5):
    
    for idx, item in enumerate(pipe):
        # discard the first image
        if idx == 0:
            time.sleep(value)
            continue
        
        # yield once captured
        yield item
        
        # sleep before the next capture
        time.sleep(value)

