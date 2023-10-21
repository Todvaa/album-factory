# Album factory Backend 

## Introduction
Photo studios produce thousands of albums yearly. This project helps to automate routine work of managers.

## Features
- Photosets uploading via cloud link
- Faces and properties recognition (face vector, exposition, peoples count, etc)
- Classification by selected properties
- Matching photos to right places in the layout template of album
- Creating complete layout
- Collecting feedback from customers 
- Editor for album review

## Structure
- Order controller + api <[ReadMe](https://github.com/Todvaa/album-factory/blob/master/data_controller/README.md)>  
Aggregated service to provide data to front via api and control order/album state
- Downloader <[ReadMe](https://github.com/Todvaa/album-factory/blob/master/photos_downloader/README.md)>  
Gets photos from remote sources
- Processor <[ReadMe](https://github.com/Todvaa/album-factory/blob/master/photos_processor/README.md)>  
Recognises and classifies photos
- Db  
Domain entity storage
- S3  
Photos storage
- Queue  
Interservice messaging
- Cache
- Web server

## Launch
1. Install:
* <a href=https://www.docker.com/get-started>Docker</a>
* <a href=https://docs.docker.com/compose/install/>Docker-compose</a>
2. Create and fill in ".env"
<br><pre>cp .env.dist .env</pre><br>
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=album_factory
POSTGRES_USER=album_factory
POSTGRES_PASSWORD=album_factory
DB_HOST=db # database container name
DB_PORT=5432

RABBITMQ_DEFAULT_USER=album_factory
RABBITMQ_DEFAULT_PASS=album_factory
RABBITMQ_PORT=5672

MINIO_ROOT_USER=album_factory
MINIO_ROOT_PASSWORD=album_factory
MINIO_PORT=9000

#dev/test/prod
APP_ENV=dev
SECRET_KEY= # Django secret key
```
3. Collect containers.
<br><pre>docker-compose up --build</pre><br>

## OpenApi 3 documentation
Generating a local file:
```command line
python manage.py generateschema --file ../api.yml
```
Web interface: http://localhost/openapi

JSON format: http://localhost/openapi/?format=openapi-json

## RabbitMQ
Web interface: http://localhost:15672
