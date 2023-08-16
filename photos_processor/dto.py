class Photo:
    def __init__(self, name, remote_url):
        self.name = name
        self.face_count = 0
        self.remote_url = remote_url
        self.vectors = []
        self.is_eyes_open = []

    def append_vector(self, vector):
        self.vectors.append(vector)
        self.face_count += 1

        return self


class Person:
    def __init__(self, file_name, vector):
        self.photo_names = [file_name]
        self.vectors = [vector]
        self.average_vector = None

    def __calculate_avg_vector(self):
        self.average_vector = sum(self.vectors) / len(self.vectors)

    def add_photo(self, file_name, vector):
        self.photo_names.append(file_name)
        self.vectors.append(vector)
        self.__calculate_avg_vector()
