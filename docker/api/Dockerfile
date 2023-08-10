FROM python:3.11-slim
WORKDIR /app

COPY ./api/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt --no-cache-dir --no-input

COPY ./api /app
COPY ./shared /app/shared
COPY ./docker/api/entrypoint /app/entrypoint
RUN chmod +x /app/entrypoint