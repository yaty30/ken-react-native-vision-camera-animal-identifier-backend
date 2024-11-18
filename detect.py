import base64
import time
from inference.models.utils import get_roboflow_model
import numpy as np
import cv2
from datetime import datetime
import os
from inference_sdk import InferenceHTTPClient
import io, base64
from PIL import Image , ImageFile, ImageDraw, ImageFont
from pydantic import BaseModel
from typing import Annotated
from io import BytesIO 

def detection(image_data, confidence, threshold):
    tiger_model = ("my_first_project-jtcqt", 2)
    
    model_info = tiger_model
    model = get_roboflow_model(
        model_id="{}/{}".format(model_info[0], model_info[1]),
        #Replace ROBOFLOW_API_KEY with your Roboflow API Key
        api_key="dYvAmlyG8pw3rxfRuzOs"
    )

    start_time = time.time()
    res = []
    try:
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image_bytes = base64.b64decode(image_data)
        image_stream = BytesIO(image_bytes)

    except Exception as e:
        print(e)
        return res
    
    results = model.infer(image=image_stream, confidence=confidence, iou_threshold=threshold)
    for result in results:
        # Check if the result has predictions
        if hasattr(result, 'predictions'):
            for prediction in result.predictions:
                x_center = prediction.x
                y_center = prediction.y
                width = prediction.width
                height = prediction.height
                
                end_time = time.time()
                elapsed_time = end_time - start_time

                data = {
                    "x": x_center,
                    "y": y_center,
                    "width": width,
                    "height": height,
                    "object": {
                        "title": prediction.class_name,
                        "description": "good"
                    },
                    "confidence": prediction.confidence,
                    "elapsed_time": elapsed_time
                }
                
                res.append(data)
        else:
            print("No predictions found in this result.")
    return res
    