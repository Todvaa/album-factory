from typing import Optional


class Photo:
    def __init__(self, name: str, remote_url: str):
        self.name: str = name
        self.face_count: int = 0
        self.remote_url: str = remote_url
        self.vectors: list = []
        self.focus: Optional[float] = None
        self.description: Optional[str] = None
        self.type: Optional[str] = None
        self.horizont: Optional[int] = None

    def append_vector(self, vector):
        self.vectors.append(vector)
        self.face_count += 1

        return self


class Person:
    def __init__(self, file_name: str, vector):
        self.photo_names = [file_name]
        self.vectors = [vector]
        self.average_vector = None

    def __calculate_avg_vector(self):
        self.average_vector = sum(self.vectors) / len(self.vectors)

    def add_photo(self, file_name: str, vector):
        self.photo_names.append(file_name)
        self.vectors.append(vector)
        self.__calculate_avg_vector()
