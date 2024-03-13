# Use the official PyTorch container image as the base image
FROM pytorch/torchserve:0.9.0-cpu

# Set the working directory inside the container
WORKDIR /home/model-server

# Copy the model_store directory into the container
COPY model-store model-store
COPY config.properties config.properties
COPY requirements.txt requirements.txt

RUN python3 -m pip install -r requirements.txt

# Set environment variables
ENV LOG_LOCATION=/home/model-server/logs

# Expose ports for TorchServe and gRPC
EXPOSE 8080 7070 8081

# Start TorchServe
CMD ["torchserve", "--start", "--model-store", "model-store", "--ts-config", "config.properties"]
