from typing import Union, Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw
import json
import io
from inference.models.utils import get_roboflow_model
from typing import List, Any
import base64
import random
from io import BytesIO
from prompt import Chat
import os
from identifier import App
from data import Fishes
import time
from customDetection import Detect

app = FastAPI()

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
import random

@app.get("/download")
async def download_file():
    file_path = "/Users/jamesyip/Desktop/Codes/VisionCamera_V2/react-native-vision-camera-animal-identifier/android/app/build/outputs/apk/release/app-release.apk"  # Replace with your file path
    return FileResponse(file_path, media_type='application/octet-stream', filename="camera.apk")


@app.get("/user")
def read_root():
    return {"Hello": "World"}

class Base64Item(BaseModel):
    data: str
    target: int
    terminated: bool

@app.post("/postData")
def frame(item: Base64Item):
    print(item)
    data = "123"
    return data

class TalkItem(BaseModel):
    id: int
    timestamp: int
    message: str

@app.post("/talk")
def talk(item: TalkItem):
    res = Chat().send(item.message)
    res = json.loads(res)
    # if 'action_found' in res:
    #     print(f"Has Action: {res['action_found']}")
    # if 'objective' in res:
    #     print(f"Objective: {res['objective']}")
    # if 'target' in res:
    #     print(f"Action Target: {res['target']}")

    response_body = {
        "id": item.id,
        "message": res['response_message'],
        "timestamp": 0,
        "from": 1,
        "initiate": False,
        "target": {}
    }

    if 'action_found' in res:
        if 'objective' in res:
            if res['action_found'] == 'true':
                if res['objective'] == 'find animal':
                    response_body["initiate"] = True
                    response_body["target"] = res['target']
        
    if 'target' in res:
        if 'name' in res['target']:
            response_body['target'] = res['target']
        else:
            response_body["target"]["name"] = ""
            response_body["target"]["nature"] = ""

    
    print(response_body)
    return response_body

class Target(BaseModel):
    name: str
    nature: str

class Base64Item(BaseModel):
    data: str
    target: Optional[Target]
    terminated: bool

@app.post("/receiveFrame")
def frame(item: Base64Item):
    start = time.time()
    time_count = 0
    res = []
    
    print(f"terminated: ${item.terminated}")
    if item.terminated:
        end = time.time()
        print(round(end-start, 2))
        return res

    base64_string = item.data

    if base64_string.startswith("data:image/jpeg;base64,"):
        base64_string = base64_string.split(",")[1]

    # Decode the Base64 string
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))    

    # Rotate the image
    rotated_image = image.rotate(-90, expand=True)

    # Process the rotated image for detection
    # detection_results = App().initiate_by_image(rotated_image)
    # for (x, y, width, height) in detection_results:
    #     res.append({
    #         "id": random.randint(100000, 9999999),
    #         "x": int(y),
    #         "y": int(x),
    #         "width": int(width),
    #         "height": int(height),
    #         "object": Fishes().get_random_target(),
    #         "confident": round(random.uniform(0.55, 0.9), 2)
    #     })
    
    # Ken's version
    detection_results = Detect().main(base64_string)
    print(detection_results)

    end = time.time()
    print(round(end-start, 2))
    return res

# uvicorn app:app --host 192.168.0.188 --port 8000 --reload

if __name__ == "__main__":
    
    # Inference image to find faces
    # model_name = "animal-detection-jvsw5"
    # model_version = "1"
    # model = get_roboflow_model(
    #     model_id="{}/{}".format(model_name, model_version),
    #     #Replace ROBOFLOW_API_KEY with your Roboflow API Key
    #     api_key="dYvAmlyG8pw3rxfRuzOs"
    # )
    # Detect().model = model
    
    os.system("uvicorn app:app --host 192.168.0.188 --port 8000 --reload")