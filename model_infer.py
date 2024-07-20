import numpy as np
from collections import namedtuple

def infer(model:object, img:str|np.ndarray, conf:float=0.5) -> object:
    '''## Example
    from ultralytics import YOLO
    
    md = YOLO("yolov8n.pt")

    infer(md,"images/IMG_9206.JPG",0.8)

    ## Returns
    object: contains all the results for the image.
    '''

    res = model(img, conf=conf)

    out = namedtuple("out", ["boxes", "masks", "names"])
    
    return out(res[0].boxes, res[0].masks, res[0].names)