class Photo:
    def __init__(self, name):
        self.name = name
        self.face_count = 0
        self.remote_url = None
        self.vectors = []

    def set_remote_url(self, remote_url):
        self.remote_url = remote_url

        return self

    def append_vector(self, vector):
        self.vectors.append(vector)
        self.face_count += 1

        return self
