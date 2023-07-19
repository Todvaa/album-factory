FROM python:3.11-slim
WORKDIR /app
COPY ./factory_clients/requirements.txt ./
RUN pip3 install -r ./requirements.txt --no-cache-dir --no-input
COPY ./factory_clients .