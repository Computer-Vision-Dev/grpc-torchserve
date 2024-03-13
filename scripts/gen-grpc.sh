#!/bin/bash

python -m grpc_tools.protoc \
    -I src/googleapis \
    --proto_path=src/proto/ \
    --python_out=src/grpc_python \
    --grpc_python_out=src/grpc_python \
    src/proto/inference.proto src/proto/management.proto
