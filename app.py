from typing import Union, Optional
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw
import json
import io
from typing import List, Any
import base64
import random
from io import BytesIO
from prompt import Chat
from identifier import App
from data import Fishes

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

@app.get("/")
def read_root():
    return {"Hello": "World"}

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
    res = []
    if item.terminated:
        return res

    # base64_string = item.data
   
    # if base64_string.startswith("data:image/jpeg;base64,"):
    #     base64_string = base64_string.split(",")[1]

    # # Decode the Base64 string
    # image_data = base64.b64decode(base64_string)
    # image = Image.open(BytesIO(image_data))
    
    # rotated_image = image.rotate(-90, expand=True)

    # # rotated_image.save("output_image.jpg", format="JPEG")

    # width, height = rotated_image.size

    # res = App().by_base64(base64_string) # should be returned in an array.
    
    # print(res)

    # return {
    #     'x': res.x, # X axis of target identified
    #     'y': res.y, # Y axis of target identified
    #     'width': res.width, # size of the target identified
    #     'height': res.height, # size of the target identified
    #     'object': {
    #         'title': 'Clown Fish', # title of the target identified
    #         # description of the target found
    #         'description': 'The clownfish can be many different colours, depending on its species, including yellow, orange, red, and black. Most have white details. They are smaller fish, with the smallest around 7 to 8cm long and the longest 17cm long'
    #     },
    #     'confident': 0.76 # accuracy score for found target
    # }

    count = random.randint(1, 3)
    size = random.randint(55, 120)
    for _ in range(1, count):
        obj = {
            'x': random.randint(10, 300),
            'y': random.randint(10, 250),
            'width': size,
            'height': size,
            'object': Fishes().get_random_target(),
            'confident': round(random.uniform(0.55, 0.9), 2)
        }
        res.append(obj)
    

    if item.target is not None:
        if item.target.name:
            print("Target: " + item.target.name)
            name = item.target.name.capitalize()
            res = [target for target in res if target["object"]["title"] == name]
    print(res)
    return res

# uvicorn app:app --host 192.168.0.188 --port 8000 --reload