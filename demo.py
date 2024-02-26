import cv2
from src.grpc_python import infer, get_inference_stub
import json
from typing import Dict

MODEL_NAME = "densenet161"
MODEL_VERSION = "1.0"
# MODEL_VERSION = None # will use default version

path = "./images/kitten.jpg"

image = cv2.imread(path)
suc, image_enc = cv2.imencode('.jpg', image)
if suc:
    image_bytes = image_enc.tobytes()
    stub = get_inference_stub(
        host="localhost",
        port=7070
    )
    result: bytes = infer(
        stub=stub,
        model_name=MODEL_NAME,
        model_version=MODEL_VERSION,
        model_input=image_bytes
    )

    prediction: Dict = json.loads(result)
    
    print("Prediction: \n", prediction)
