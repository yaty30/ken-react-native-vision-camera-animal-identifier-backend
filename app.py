from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from PIL import Image, ImageDraw
import json
import io
import base64
import random
import ssl
import get_cert
from prompt import Chat

app = FastAPI()

# Allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

# Load SSL certificate chain and private key
try:
    ssl_context.load_cert_chain(
        certfile='/Users/jamesyip/Desktop/Kens/backend/certificate.pem', 
        keyfile='/Users/jamesyip/Desktop/Kens/backend/private_key.pem'
    )
except ssl.SSLError as e:
    print(f"SSL certificate loading error: {e}")


def draw_square_on_image(base64_string):
    # Remove any header before decoding
    if base64_string.startswith('data:image'):
        base64_string = base64_string.split(',', 1)[1]

    # Pad the base64 string if needed
    missing_padding = len(base64_string) % 4
    if missing_padding != 0:
        base64_string += '=' * (4 - missing_padding)

    try:
        # Decode the base64 string to bytes
        image_bytes = base64.b64decode(base64_string)

        # Load the image from the decoded bytes
        image = Image.open(io.BytesIO(image_bytes))

        # Get image dimensions
        width, height = image.size

        # Fixed size for the square
        size = 50

        # Generate random coordinates for the square
        x1, y1 = random.randint(0, width - size), random.randint(0, height - size)

        # Create an ImageDraw object
        draw = ImageDraw.Draw(image)

        # Draw a square with specified line thickness
        for i in range(4):
            draw.line([(x1 + i, y1), (x1 + size + i, y1)], fill='red', width=1)  # Top line
            draw.line([(x1 + size, y1 + i), (x1 + size, y1 + size + i)], fill='red', width=1)  # Right line
            draw.line([(x1 + size + i, y1 + size), (x1 + i, y1 + size)], fill='red', width=1)  # Bottom line
            draw.line([(x1, y1 + size + i), (x1, y1 + i)], fill='red', width=1)  # Left line

        # Convert the modified image to a base64 string
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        base64_modified_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return f"data:image/png;base64,{base64_modified_image}"

    except Exception as e:
        print(f"An error occurred: {e}")

# Create a Pydantic model to represent the data in the POST body
class Item(BaseModel):
    id: int
    timestamp: int
    footageFrame: str

@app.post("/streamFeed")
async def feed(item: Item):
    return {
        "id": item.id,
        "timestamp": 0,
        "footageFrame": draw_square_on_image(item.footageFrame)
    }


@app.get("/")
def read_root():
    return {"Hello": "World"}

class ReceiveItem(BaseModel):
    base_64_img: str

@app.post("/receive")
def receive(item: ReceiveItem):
    print(item.base_64_img)
    return {
        "status": "received"
    }

class TalkItem(BaseModel):
    id: int
    timestamp: int
    message: str

@app.post("/talk")
def talk(item: TalkItem):
    res = Chat().Send(item.message)
    res = json.loads(res)
    if 'action_found' in res:
        print(f"Has Action: {res['action_found']}")
    if 'objective' in res:
        print(f"Objective: {res['objective']}")
    if 'target' in res:
        print(f"Action Target: {res['target']}")

    return {
        "id": item.id,
        "message": res['response_message'],
        "timestamp": 0,
        "from": 1
    }


# uvicorn app:app --host 192.168.0.188 --port 8000 --reload --ssl-keyfile /Users/jamesyip/Desktop/Kens/backend/private_key.pem --ssl-certfile /Users/jamesyip/Desktop/Kens/backend/certificate.pem