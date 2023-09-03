from typing import Optional, List


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
    def __init__(self, photo_s3_path: str, vector):
        self.photos_s3_path: List[str] = [photo_s3_path]
        self.vectors: list = [vector]
        self.average_vector = None

    def __calculate_avg_vector(self):
        self.average_vector = sum(self.vectors) / len(self.vectors)

    def add_photo(self, photo_s3_path: str, vector):
        self.photos_s3_path.append(photo_s3_path)
        self.vectors.append(vector)
        self.__calculate_avg_vector()
