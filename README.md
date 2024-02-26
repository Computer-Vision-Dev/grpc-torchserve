# GRPC and TorchServe

## Installation
Create venv:
```
python -m venv venv

source venv/bin/activate
```

Install dependencies:
```
cd torchserve-demo/
pip install .
```

Install torch package:
```
# cpu
install-torch

# cuda 10.2
install-torch --cuda cu102

# cuda 12.1
install-torch --cuda cu121
```
For more information and see support cuda versions:
```
install-torch --help
```
> Required python >= 3.10 or could change python version inside `pyproject.toml`

## Quickstart
Download `densenet161` checkpoint:
```
cd checkpoints/
wget https://download.pytorch.org/models/densenet161-8d451a50.pth
cd ..
```

1. Create model .mar file in `model_store`
```
torch-model-archiver \
--model-name densenet161_1 \
--version 1.0 \
--model-file src/models/densenet_161/model.py \
--serialized-file checkpoints/densenet161-8d451a50.pth \
--export-path model_store \
--extra-files index_to_name.json \
--handler src/handlers/custom_handler.py
```
> A convention to name model `.mar` file is `{model_name}_{version}`. In above command, `model_name` is "densenet161" and `version` is "1". If you have version 2 for model densenet161, `--model-name` should be `densenet161_2` and `--version` is `2.0`.

2. Start torchserve:
```
LOG_LOCATION=logs torchserve --start --model-store model_store
```
> LOG_LOCATION is an environment variable that specify where torch serve should write logs to. In above command, torchserve write logs in `logs` directory.

3. Register model `densenet`:
```
curl -X POST "http://localhost:8081/models?model_name=densenet161&url=densenet161_1.mar&initial_workers=1"
```
> When register different versions for the same model, the `model_name` parameter should be the same. `url` parameter is the model `.mar` file. `initial_workers` is the number of workers registered to this model. To register version 2 for densenet161, the query parameters should be: `models?model_name=densenet161&url=densenet161_2.mar&initial_workers=1`. For more information: [Register a model](https://pytorch.org/serve/management_api.html#register-a-model)

4. Set default version for model:
```
# set densenet161 version 1 as default
curl -X PUT "http://localhost:8081/models/densenet161/1.0/set-default"
```

5. Inference via GRPC
```
python demo.py
```

## How to use grpc
```
import cv2
import json
from typing import Dict

# import grpc client
from src.grpc_python import infer, get_inference_stub

# define model name and version
MODEL_NAME = "densenet161"
MODEL_VERSION = "1.0"

# Read image and convert to bytes
path = "./images/kitten.jpg"
image = cv2.imread(path)
suc, image_enc = cv2.imencode('.jpg', image)
image_bytes = image_enc.tobytes()

# Infer gprc
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

# Decode result
prediction: Dict = json.loads(result)
```

> `prediction` result should be the same as the result return from model handler

## About pyproject.toml
All dependencies required in these files:
```
dependencies = {file = [
    "requirements/torchserve.txt", 
    "requirements/grpc.txt", 
    "requirements/optional.txt", 
]}
```
`requirements/optional.txt` contains dependencies package depend on the needs. Can be overwrited. If you need fastapi, pillow, scikit-learn,... add them to `optional.txt`

Pytorch need to install separately using script like we did in `Installation`:
```
[project.scripts]
install-torch = "src.ts_scripts.install_dependencies:main"
```

## To see all API of torchserve
Go to this [website](https://mermade.github.io/openapi-gui/)

Go to `Upload` -> Copy all contents in `api-docs/management.json` or `api-docs/inference.json` -> Paste it on the big white box -> Click `Load Definition`

Go to `Main` tab to see all the endpoints and parameters.

