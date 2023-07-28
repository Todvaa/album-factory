import json

from scipy.spatial.distance import pdist


class AbstractClassificator:

    def __init__(self, vectors):
        self.vectors = vectors

    def run(self):
        pass


class Classificator(AbstractClassificator):

    def run(self):
        vector_pairs = {}
        for first_file, first_vector in self.vectors.items():
            if first_vector is not None:
                for second_file, second_vector in self.vectors.items():
                    if second_vector is not None:
                        key = [first_file, second_file]
                        key.sort()
                        key_str = json.dumps(key)
                        if (first_file != second_file) and (key_str not in vector_pairs):
                            vector_pairs[key_str] = pdist([first_vector, second_vector], 'euclidean')

        persons = []
        for files_str, match in vector_pairs.items():
            if match < 0.6:
                photos = json.loads(files_str)
                was_added = False
                for person in persons:  # todo handle duplicates: in the future
                    if photos[0] in person:
                        was_added = True
                        person.append(photos[1])
                    elif photos[1] in person:
                        was_added = True
                        person.append(photos[0])
                if not was_added:
                    persons.append(photos)
        # todo: добавлять тех, кто не похож ни на кого
        # todo: дабавляются дубликаты
        return persons
