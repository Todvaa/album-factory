# Album factory Backend Data Controller

## Api
Two types of authorization. For the studio and for their customers ("Studio" and "Order" entities).
Both authorizations used JWT. Studios can add "School" and "Order" entities.
The password for customer authorization is generated and issued by the Studio

## Connsumers
#### photos_downloaded
Receives the "order photos downloaded" event.
Changes the order status to "portraits_processing".
```command line
python manage.py consume_queue_photos_downloaded
```
#### photos_processed
Receives the "order photos processed" event.
Create "Photo",  "PersonStudent" entities and relation between them in "PhotoPersonStudent" entity.
Changes the order status to "portraits_processed".
Send templates for the front to the next queue.
```command line
python manage.py consume_queue_photos_processed
```

## OpenApi documentation
- [OpenApi Doc](https://github.com/Todvaa/album-factory/blob/master/api.yml)  
- Generating a local file:
```command line
python manage.py generateschema --file ../api.yml
```
- Web interface: http://localhost/openapi
- JSON format: http://localhost/openapi/?format=openapi-json
