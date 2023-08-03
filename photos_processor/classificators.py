from abc import ABC, abstractmethod

from scipy.spatial.distance import pdist

from constants import EQUALITY_FACTOR


class AbstractClassificator(ABC):

    def __init__(self, vectors: dict):
        self.vectors = vectors

    @abstractmethod
    def run(self):
        pass


class Classificator(AbstractClassificator):

    def __average_vector(self, vectors: list):
        return sum(vectors) / len(vectors)

    def run(self):
        unclassified_vectors = self.vectors.copy()
        persons = []
        while len(unclassified_vectors) != 0:
            first_file, first_vector = unclassified_vectors.popitem()
            person = {'photos': [first_file, ], 'vectors': [first_vector, ]}
            to_remove = []
            for second_file, second_vector in unclassified_vectors.items():
                if pdist([first_vector, second_vector], 'euclidean') < EQUALITY_FACTOR:
                    person['photos'].append(second_file)
                    person['vectors'].append(second_vector)
                    to_remove.append(second_file)

            for key in to_remove:
                unclassified_vectors.pop(key)

            persons.append(person)

        for person in persons:
            person['vector'] = self.__average_vector(vectors=person['vectors']).tolist()
            person.pop('vectors')

        return persons
