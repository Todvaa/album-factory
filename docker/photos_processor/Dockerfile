FROM python:3.11-slim
WORKDIR /app

# This flag is important to output python logs correctly in docker!
ENV PYTHONUNBUFFERED 1
# Flag to optimize container size a bit by removing runtime python cache
ENV PYTHONDONTWRITEBYTECODE 1

# Dlib intallation
RUN apt-get update \
    && apt install -y cmake build-essential g++ \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install dlib

COPY ./photos_processor/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt --no-cache-dir --no-input

RUN apt-get update \
    && apt install -y libgl1-mesa-glx ffmpeg libsm6 libxext6

COPY ./photos_processor /app/photos_processor
COPY ./shared /app/shared

ENV PYTHONPATH "/app"

CMD python /app/photos_processor/main.py