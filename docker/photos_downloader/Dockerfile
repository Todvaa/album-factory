FROM python:3.11-slim
WORKDIR /app

# This flag is important to output python logs correctly in docker!
ENV PYTHONUNBUFFERED 1
# Flag to optimize container size a bit by removing runtime python cache
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./photos_downloader/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt --no-cache-dir --no-input

COPY ./photos_downloader /app/photos_downloader
COPY ./shared /app/photos_downloader/shared

ENV PYTHONPATH "/app"
CMD python photos_downloader/main.py