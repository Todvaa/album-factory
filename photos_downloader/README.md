# Album factory Backend Photos Downloader

## Description
Receives the "photo upload order" event. 
Downloads photos from the cloud using a link from a message. 
Uploads photos to S3 storage.
Sends messages further in the queue ("photos_downloaded" and "photos_processing").
