from ultralytics import YOLO
import cv2
import base64
import time
from tqdm import tqdm
from inference.models.utils import get_roboflow_model
import cv2
import base64
from PIL import Image, ImageFile
from pydantic import BaseModel
from io import BytesIO
import os
import pickle

class Train():
    def __init__(self, yaml, epochs, imgsz):
        self.training_session = {
            "yaml": yaml, "epochs": epochs
        }

        self.config = {
            "data": yaml,
            "epochs": epochs,
            "imgsz": imgsz # should be dynamic value based on current image
        }
    
    def yolo_training_session(self):
        command = f'yolo task=detect mode=train data={self.training_session["yaml"]} model=yolov8n.pt epochs={self.training_session["epochs"]}'
        # print(command)
        os.system(command)

    def start(self):
        self.yolo_training_session()
        
        self.custom_model = self.model.train(
            data=self.config["data"], 
            epochs=self.config["epochs"], 
            imgsz=self.config["imgsz"]
        )


class Prepare:
    def __init__(self, root, model_name, data):
        self.model_name = model_name
        self.data = data
        self.root = root
        self.dataset_root = f"{self.root}/datasets/{self.model_name}"
        self.export_path = self.setup_directories()

    def setup_directories(self):
        paths = {
            "parent": f"{self.dataset_root}",
            "yaml": f"{self.root}/yaml/{self.model_name}",
            "train": {
                "main": f"{self.dataset_root}/train",
                "images": f"{self.dataset_root}/train/images",
                "labels": f"{self.dataset_root}/train/labels",
            },
            "val": {
                "main": f"{self.dataset_root}/val",
                "images": f"{self.dataset_root}/val/images",
                "labels": f"{self.dataset_root}/val/labels",
            }
        }
        for _, path in paths.items():
            if isinstance(path, dict):
                for subpath in path.values():
                    os.makedirs(subpath, exist_ok=True)
            else:
                os.makedirs(path, exist_ok=True)
        return paths

    def start(self):
        self.class_id = 0

        for item in tqdm(data):
            self.model_info = item["model"]
            self.model = get_roboflow_model(
                model_id="{}/{}".format(self.model_info[0], self.model_info[1]),
                #Replace ROBOFLOW_API_KEY with your Roboflow API Key
                api_key="dYvAmlyG8pw3rxfRuzOs"
            )

            os.system("cls")
            print(f"Current Target: {item['target']}")
            print(f"Roboflow Model: {self.model_info[0]} v{self.model_info[1]}")
            print(f"Video Source: {item['vid_src']}")
            print("===========================================================================")
            self.extract_frames(item["vid_src"], item["target"])
            self.dataset()

            self.class_id += 1
            print(self.class_id)
            input("next...")
        
        os.system("cls")
        print(f"Preparation Completed: {[item['target'] for item in data]}")
        print("Generating .yaml")
        yaml = self.generarte_yaml()
        
        print("===========================================================================")
        print("Training Model")
        train_instance = Train(yaml, 100, 1024)
        train_instance.start()
        

    def extract_frames(self, src_vid, current_target, desired_fps=10):
        source = cv2.VideoCapture(src_vid)
        original_fps = source.get(cv2.CAP_PROP_FPS)
        frame_interval = int(original_fps / desired_fps)
        total_frames = int(source.get(cv2.CAP_PROP_FRAME_COUNT))
        switch_threshold = int(total_frames * 0.66)

        success, image = source.read()
        count = 0
        saved_count = 0
        export_src = self.export_path["train"]["images"]
        current_export_type = "train"
        
        with tqdm(total=total_frames, desc=f"Extracting frames - {current_target} - {current_export_type}", unit="frame") as pbar:
            while success:
                if count >= switch_threshold:
                    export_src = self.export_path["val"]["images"]
                    current_export_type = "val"

                if count % frame_interval == 0:
                    cv2.imwrite(f"{export_src}/{current_target}_Frame_{saved_count}.jpg", image)
                    saved_count += 1

                success, image = source.read()
                count += 1
                pbar.update(1)
        
        source.release()

    class IdentifiedObjectModel(BaseModel):
        class_id: int
        center_x: float
        center_y: float
        width: float
        height: float
        
        # Class ID: 0
        # Center X: 0.495703125 - ObjX / ImgW
        # Center Y: 0.48333333333333334 - ObjY / ImgH
        # Width: 0.68046875 - ObjXWP / ImgW
        # Height: 0.6027777777777777 - ObjYHP / ImgH

    # Prepare dataset for YOLO, utilising ROBOFLOW Models
    def detection(self, image_data, image_path, label_path, confidence=0.5, threshold=0.5):
        res = []

        with Image.open(image_path) as img:
            src_width, src_height = img.size
        
        try:
            ImageFile.LOAD_TRUNCATED_IMAGES = True
            image_bytes = base64.b64decode(image_data)
            image_stream = BytesIO(image_bytes)
            
            results = self.model.infer(image=image_stream, confidence=confidence, iou_threshold=threshold)

        except Exception as e:
            print(e)
            return res
        
        for result in results:
            # Check if the result has predictions
            if hasattr(result, 'predictions'):
                for prediction in result.predictions:
                    width = prediction.width
                    height = prediction.height

                    x1 = prediction.x - (width / 2)
                    x2 = prediction.x + (width / 2)
                    y1 = prediction.y - (height / 2)
                    y2 = prediction.y + (height / 2)

                    center_x = prediction.x / src_width
                    center_y = prediction.y / src_height
                    normalised_width = (x2 - x1) / src_width
                    normalised_height = (y2 - y1) / src_height
                    
                    data = {
                        "class_id": self.class_id,
                        "center_x": center_x,
                        "center_y": center_y,
                        "width": normalised_width,
                        "height": normalised_height,
                    }
                    res.append(data)
            # else:
            #     print("No predictions found in this result.")

        with open(label_path, 'w') as ep:
            data = ""
            for item in res:
                for _, value in item.items():
                    data += str(value) + " "
            ep.write(data)

    def image_to_base64(self, image_path):
        # Open the image using PIL
        with Image.open(image_path) as image:
            # Create a BytesIO buffer to hold the image data
            buffered = BytesIO()
            # Save the image to the buffer in JPEG format
            image.save(buffered, format="JPEG")
            # Encode the image data to base64
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return img_base64

    def create_labels_cache(self, image_src, label_src, cache_file):
        data = {}

        for filename in os.listdir(image_src):
            if filename.endswith(('.jpg', '.png')):
                image_path = os.path.join(image_src, filename).replace("\\", "/")
                label_path = os.path.join(label_src, os.path.splitext(filename)[0] + '.txt').replace("\\", "/")

                # Get image size
                with Image.open(image_path) as img:
                    width, height = img.size

                # Read label file
                if os.path.exists(label_path):
                    with open(label_path, 'r') as f:
                        labels = f.read().strip().splitlines()
                else:
                    labels = []

                # Store information
                data[filename] = {
                    'image_path': image_path,
                    'label_path': label_path,
                    'width': width,
                    'height': height,
                    'labels': labels
                }

        # Write cache to file
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)

    def dataset(self):
        image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
        types = ['train', 'val']
        folder_paths = [self.export_path['train'], self.export_path['val']]

        for idx, path in enumerate(folder_paths):
            images = sorted([f for f in os.listdir(path['images']) if f.lower().endswith(image_extensions)])

            for image in tqdm(images, desc=f"Identifying object for {types[idx]}", unit="image"):
                image_src = f"{path['images']}/{image}"
                if os.path.isfile(image_src):
                    label_src = f"{path['labels']}/{image.replace('jpg', 'txt')}"
                    image_data = self.image_to_base64(image_src)
                    self.detection(image_data, image_src, label_src)

            self.create_labels_cache(
                path['images'],
                path['labels'],
                f"{path['main']}/labels.cache"
            )

    def generarte_yaml(self):
        targets = [item['target'] for item in self.data]
        yaml_src = f"./yaml/{self.model_name}/{self.model_name}.yaml"
        with open(yaml_src, "w") as yaml:
            lines = [
                f"# {self.model_name}.yaml\n\n", "# Paths\n",
                f"path:  C:/Users/James/Desktop/Codes/YOLO/datasets/{self.model_name}  # root dataset directory\n",
                f"train: {self.export_path['train']['images']}\n",
                f"val: {self.export_path['val']['images']}\n\n"
                "# Number of classes\n",
                f"nc: {len(targets)}\n\n",
                "# Class names\n",
                f"names: {targets}"
            ]

            for line in lines:
                yaml.write(line)

        return yaml_src
            

if __name__ == "__main__":
    fish_model = ("mergetest-tl3d3", 1)
    zebra_model = ("zebra-htuxd", 1)
    tiger_model = ("my_first_project-jtcqt", 2)
    giraffe_model = ("projetgirafe", 3)
    lionfish_model = ("lionfish-6f19u", 1)

    data = [
        { "target": "clownfish", "model": fish_model, "vid_src": r"C:\Users\James\Desktop\Codes\HaarCascade\source_frames\clownfish.mp4" },
        { "target": "tiger", "model": tiger_model, "vid_src": r"C:\Users\James\Desktop\Codes\HaarCascade\source_frames\tiger.mp4" },
        { "target": "lionfish", "model": lionfish_model, "vid_src": r"C:\Users\James\Desktop\Codes\HaarCascade\source_frames\lionfish.mp4" },
    ]

    prepare = Prepare(f"C:/Users/James/Desktop/Codes/YOLO", "animal-classifier", data)
    prepare.start()