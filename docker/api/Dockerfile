FROM python:3.11-slim
WORKDIR /app

# This flag is important to output python logs correctly in docker!
ENV PYTHONUNBUFFERED 1
# Flag to optimize container size a bit by removing runtime python cache
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./data_controller/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt --no-cache-dir --no-input

COPY ./data_controller /app
COPY ./shared /app/shared
COPY ./docker/data_controller/entrypoint /app/entrypoint
RUN chmod +x /app/entrypoint