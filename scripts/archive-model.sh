#!/bin/bash

torch-model-archiver \
--model-name densenet161_1 \
--version 1.0 \
--model-file src/models/densenet_161/model.py \
--serialized-file checkpoints/densenet161-8d451a50.pth \
--export-path model_store \
--extra-files index_to_name.json \
--handler src/handlers/custom_handler.py
