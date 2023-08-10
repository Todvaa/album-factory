FROM python:3.11-slim
WORKDIR /app

COPY ./photos_downloader/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt --no-cache-dir --no-input

COPY ./photos_downloader /app
COPY ./shared /app/shared

CMD python /app/main.py