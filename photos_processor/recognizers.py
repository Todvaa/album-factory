import os
from abc import ABC, abstractmethod

import cv2
import face_recognition


class AbstractRecognizer(ABC):
    def __init__(self, dir_path: str):
        self.dir_path = dir_path

    @abstractmethod
    def _handle(self, file_path: str):
        pass

    def __get_photos_list(self):
        return os.listdir(self.dir_path)

    def run(self) -> dict:
        files = self.__get_photos_list()
        vectors = {}
        for file in files:
            vector = self._handle(os.path.join(self.dir_path, file))
            if vector is not None:
                vectors[file] = vector
            # todo: если none, то запись в лог, что у фото не распознано лицо
        return vectors


class Recognizer(AbstractRecognizer):
    def _handle(self, file_path: str):
        img = cv2.imread(file_path)
        vector_faces = face_recognition.face_encodings(img)
        if len(vector_faces) == 1:
            vector = face_recognition.face_encodings(img)[0]
        else:
            vector = None

        return vector
