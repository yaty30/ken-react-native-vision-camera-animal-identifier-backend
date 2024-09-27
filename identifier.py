import cv2
import base64
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DetectionResult(BaseModel):
    x: int = None
    y: int = None
    width: int = None
    height: int = None

class App:
    trained_Haar_Cascade_dateset = "stop_data.xml"

    def initiate_by_base64(self, base64_string):
        # Decode the base64 string
        img_data = base64.b64decode(base64_string) # need to rotate the image
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            print("Failed to decode image")
            return DetectionResult()

        # Get original dimensions
        original_height, original_width = img.shape[:2]

        # Resize the image to be 8 times larger
        img = cv2.resize(img, (original_width * 8, original_height * 8), interpolation=cv2.INTER_LINEAR)

        # Convert to grayscale
        image_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Load the Haar Cascade
        stop_data = cv2.CascadeClassifier(self.trained_Haar_Cascade_dateset)
        found = stop_data.detectMultiScale(image_grey, minSize=(20, 20))

        if len(found) > 0:
            for (x, y, width, height) in found:
                # Scale back to original dimensions
                return DetectionResult(
                    x=int(x / 8), 
                    y=int(y / 8), 
                    width=int(width), 
                    height=int(height)
                )
        
        return DetectionResult()

    def by_base64(self, base64_string):
        return self.initiate_by_base64(base64_string)
