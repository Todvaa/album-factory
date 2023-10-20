# Album factory Backend Photos Processor

## Description
Receives the event from "photos_processing". 
Downloads photos from S3 storage. 
"Recognizer" finds vectors of faces in photos.
"Classificator" distributes photographs by person, comparing their vectors.
Sends data in message to a queue ("photos_processed").
