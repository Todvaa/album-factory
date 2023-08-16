import os
from abc import ABC, abstractmethod

import cv2
import face_recognition
from scipy.spatial.distance import pdist

from photos_processor.constants import MODULE_NAME
from shared.logger import logger


class AbstractRecognizer(ABC):
    def __init__(self, dir_path: str, photos: list):
        self.dir_path = dir_path
        self.photos = photos

    @abstractmethod
    def _handle(self, file_path: str):
        pass

    def run(self) -> list:
        logger.info(module=MODULE_NAME, message='Face recognition launched')
        photos_with_vectors = []
        for photo in self.photos:
            vector = self._handle(os.path.join(self.dir_path, photo.name))
            if vector is not None:
                photo.append_vector(vector=vector)
                right_eye = vector[42:48]
                left_eye = vector[36:42]
                is_eyes_open = self.is_eyes_open(left_eye, right_eye)
                photo.is_eyes_open.append(is_eyes_open)

                photos_with_vectors.append(photo)
            else:
                logger.info(
                    module=MODULE_NAME,
                    message=f'Face not recognized in photo {photo.name}'
                )
        logger.info(module=MODULE_NAME, message='Face recognition finished')

        return photos_with_vectors

    # see: https://github.com/elliotBraem/all-eyes/blob/master/all_eyes/src/utils.py
    # if either eye is closed, we will determine that a swap is needed.
    def is_eyes_open(self, left_eye, right_eye):
        left_open = self.is_eye_open(left_eye)
        right_open = self.is_eye_open(right_eye)

        if not right_open or not left_open:
            return True
        else:
            return False

    # determines if the eye is open or closed based on a ratio of top and bottom to sides of the eye
    def is_eye_open(self, eye):
        OPEN_THRESHOLD = 0.2
        # euclidean distances between vertical pairs.

        a = pdist([[eye[1]], [eye[5]]], 'euclidean')
        b = pdist([[eye[2]], [eye[4]]], 'euclidean')

        # euclidean distance between horizontal pair
        c = pdist([[eye[0]], [eye[3]]], 'euclidean')

        # compute the eye aspect ratio
        ratio = (a + b) / (2.0 * c)

        # return the eye aspect ratio
        return ratio >= OPEN_THRESHOLD


# todo: crop photos
class Recognizer(AbstractRecognizer):
    def _handle(self, file_path: str):
        img = cv2.imread(file_path)
        vector_faces = face_recognition.face_encodings(img)
        if len(vector_faces) == 1:
            vector = vector_faces[0]
        else:
            vector = None

        return vector
