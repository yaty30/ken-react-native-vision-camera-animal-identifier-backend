import cv2
import numpy as np
from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from io import BytesIO
from PIL import Image


class DetectionResult(BaseModel):
    x: int = None
    y: int = None
    width: int = None
    height: int = None

class App:
    trained_Haar_Cascade_dateset = "tiger.xml" #"stop_data.xml"

    def initiate_by_image(self, image: Image.Image):
        # Convert the PIL image to a NumPy array and then to BGR format
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        ratio = 4
        # Resize the image by 3 times
        original_size = img.shape[:2]  # Get the original height and width
        new_size = (original_size[1] * ratio, original_size[0] * ratio)  # (width, height)
        img_resized = cv2.resize(img, new_size)
        # image.save("output_image.jpg", format="JPEG")

        # Convert the resized image to grayscale
        image_grey = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

        # Load the Haar cascade classifier
        stop_data = cv2.CascadeClassifier(self.trained_Haar_Cascade_dateset)

        # Detect objects in the grayscale image
        found = stop_data.detectMultiScale(image_grey, minSize=(20, 20))

        return found
    
    def by_image(self, image: Image.Image):
        return self.initiate_by_image(image)
