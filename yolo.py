import base64
from ultralytics import YOLO
from io import BytesIO
from PIL import Image
import time
import numpy as np

model = YOLO(r"C:\Users\James\Desktop\Codes\YOLO\Models\lionfish\weights\best.pt")  # load a custom model
def run(image_np, imgsz):
    print('run')
    start = time.time()
    results = model(source=image_np, conf=0.7, imgsz=imgsz) 
    # Get the positions of detected objects
    res = []
    for result in results:
        # result.show()
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # Coordinates of the bounding box
            res.append(f"Detected object at: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
    
    end = time.time()
    print("rrun", round(end-start, 2))
    return (res, round(end-start, 2))