import base64
from http.client import HTTPException
import time

import numpy as np
from inference.models.utils import get_roboflow_model
import cv2
from inference_sdk import InferenceHTTPClient
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, File, UploadFile,Body
import io, base64
from PIL import Image , ImageFile
from pydantic import BaseModel
from typing import Annotated
from io import BytesIO
# Image path

# Load image with opencv

# Inference image to find faces
model_name = "animal-detection-jvsw5"
model_version = "1"
model = get_roboflow_model(
    model_id="{}/{}".format(model_name, model_version),
    #Replace ROBOFLOW_API_KEY with your Roboflow API Key
    api_key="dYvAmlyG8pw3rxfRuzOs"
)

class Item(BaseModel):
    image_data: str

app = FastAPI()
@app.post("/")
async def main(item):
    start_time = time.time()
    # image_path = r"C:\Users\user\data\uploaded_images\lion.jpg"
    # frame = cv2.imread(image_path)

    # Get Roboflow face model (this will fetch the model from Roboflow)


    try:
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image_bytes = base64.b64decode(item.image_data)
        # image_stream = BytesIO(image_bytes)
        # # Open the image using Pillow (PIL)
        # image = Image.open(image_stream)

    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid image data")

    results = model.infer(image=image_bytes,confidence=0.5,iou_threshold=0.5)

    # # Process results
    if results[0].predictions:
        
        prediction = results[0].predictions[0]

        
        x_center = int(prediction.x)
        y_center = int(prediction.y)
        width = int(prediction.width)
        height = int(prediction.height)

        # Calculate bounding box
        # x0 = x_center - width // 2
        # y0 = y_center - height // 2
        # x1 = x_center + width // 2
        # y1 = y_center + height // 2

        # # Annotate image (optional)
        # # cv2.rectangle(frame, (x0, y0), (x1, y1), (255, 255, 0), 10)
        # # cv2.putText(frame, "Face", (x0, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.2f} second")
        # Return prediction result
        return {
            "x": x_center,
            "y": y_center,
            "width": width,
            "height": height,
            "object": {
                "title": prediction.class_name,
                "description": "good"
            },
            "confidence": prediction.confidence
        }
    # return img
    # raise HTTPException(status_code=404, detail="No faces detected")

# if __name__ == "__main__":
#     app = FastAPI()