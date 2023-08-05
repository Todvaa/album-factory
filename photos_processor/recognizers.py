import os
from abc import ABC, abstractmethod

import cv2
import face_recognition

from constants import MODULE_NAME
from shared.logger import logger


class AbstractRecognizer(ABC):
    def __init__(self, dir_path: str, photos: list):
        self.dir_path = dir_path
        self.photos = photos

    @abstractmethod
    def _handle(self, file_path: str):
        pass

    def run(self) -> dict:
        logger.info(module=MODULE_NAME, message='Face recognition launched')
        vectors = {}
        for photo in self.photos:
            vector = self._handle(os.path.join(self.dir_path, photo.name))
            if vector is not None:
                photo.append_vector(vector=vector)
                vectors[photo.name] = vector
            else:
                logger.info(
                    module=MODULE_NAME,
                    message=f'Face not recognized in photo {photo.name}'
                )
        logger.info(module=MODULE_NAME, message='Face recognition finished')

        return vectors


# todo: crop photos
class Recognizer(AbstractRecognizer):
    def _handle(self, file_path: str):
        img = cv2.imread(file_path)
        vector_faces = face_recognition.face_encodings(img)
        if len(vector_faces) == 1:
            vector = face_recognition.face_encodings(img)[0]
        else:
            vector = None

        return vector
