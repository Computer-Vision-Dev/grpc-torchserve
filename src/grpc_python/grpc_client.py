import grpc
from typing import Tuple, Optional, Generator, Any

import src.grpc_python.inference_pb2 as inference_pb2
import src.grpc_python.inference_pb2_grpc as inference_pb2_grpc
import src.grpc_python.management_pb2_grpc as management_pb2_grpc

def get_inference_stub(host: str, port: int) -> inference_pb2_grpc.InferenceAPIsServiceStub:
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = inference_pb2_grpc.InferenceAPIsServiceStub(channel)
    return stub

def get_management_stub(host: str, port: int):
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = management_pb2_grpc.ManagementAPIsServiceStub(channel)
    return stub

def infer(
    stub: inference_pb2_grpc.InferenceAPIsServiceStub, 
    model_name: str, 
    model_version: str, 
    model_input: bytes, 
    metadata: Optional[Tuple] = None
) -> bytes:
    if metadata is None:
        metadata = (("protocol", "gRPC"), ("session_id", "12345"))
    
    input_payload = {"data": model_input}    

    response = stub.Predictions(
        inference_pb2.PredictionsRequest(
            model_name=model_name, 
            input=input_payload, 
            model_version=model_version
        ),
        metadata=metadata,
    )

    try:
        return response.prediction
    except grpc.RpcError:
        exit(1)


def infer_stream(
    stub: inference_pb2_grpc.InferenceAPIsServiceStub, 
    model_name: str, 
    model_version: str, 
    model_input: bytes, 
    metadata: Optional[Tuple] = None
) -> Generator[bytes, Any, Any]:
    if metadata is None:
        metadata = (("protocol", "gRPC"), ("session_id", "12345"))
    input_payload = {"data": model_input}
    responses = stub.StreamPredictions(
        inference_pb2.PredictionsRequest(
            model_name=model_name, 
            input=input_payload,
            model_version=model_version
        ),
        metadata=metadata,
    )

    try:
        for resp in responses:
            yield resp.prediction
    except grpc.RpcError as e:
        exit(1)
