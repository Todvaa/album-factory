import os

import cv2
import face_recognition


class AbstractRecognizer:
    def __init__(self, dir_path):
        self.dir_path = dir_path

    def handle(self, file_path):
        pass

    def get_photos_list(self):
        return os.listdir(self.dir_path)

    def run(self):
        files = self.get_photos_list()
        vectors = {}
        for file in files:
            vector = self.handle(os.path.join(self.dir_path, file))
            vectors[file] = vector

        return vectors

class Recognizer(AbstractRecognizer):
    def handle(self, file_path):
        img = cv2.imread(file_path)
        vector_faces = face_recognition.face_encodings(img)
        # todo: скипать фотку если нет лица
        if len(vector_faces) == 1:
            vector = face_recognition.face_encodings(img)[0]
        else:
            vector = None

        return vector
