# Album factory Backend Photos Downloader

## Description
Receives the event from "photos_downloading". Downloads photos from the cloud using a link from a message. Uploads photos to S3 storage.  Sends data to queue ("photos_downloaded" and "photos_processing").
