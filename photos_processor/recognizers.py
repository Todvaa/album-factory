import os


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
            vector = self.handle(file)
            vectors[file] = vector

        return vectors


class Recognizer(AbstractRecognizer):
    def handle(self, file_path):
        face_detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        img = cv2.imread('conor.jpg')
