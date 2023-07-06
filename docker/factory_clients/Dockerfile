FROM python:3.9-slim
WORKDIR /app
COPY ./factory_clients/requirements.txt ./
RUN pip3 install -r ./requirements.txt --no-cache-dir --no-input
COPY ./factory_clients .