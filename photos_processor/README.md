# Album factory Backend Photos Processor

## Description
Receives the event from "photos_processing". 
Downloads photos from S3 storage. 
"Recognizer" finds vectors of faces in photos.
"Classificator" distributes photos by person, comparing their vectors.
Sends data to the queue ("photos_processed").
