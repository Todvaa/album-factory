from abc import ABC, abstractmethod

from scipy.spatial.distance import pdist

from constants import EQUALITY_FACTOR, MODULE_NAME
from dto import Person
from shared.logger import logger


class AbstractClassificator(ABC):

    def __init__(self, photos: list):
        self.photos = photos

    @abstractmethod
    def run(self):
        pass


class Classificator(AbstractClassificator):

    def run(self):
        logger.info(module=MODULE_NAME, message='People classifier launched')
        unclassified_photos = self.photos.copy()
        persons = []
        while len(unclassified_photos) != 0:
            first_photo = unclassified_photos.pop()
            first_file, first_vector = first_photo.name, first_photo.vectors[0]
            person = Person(file_name=first_file, vector=first_vector)
            to_remove = []
            for second_photo in unclassified_photos:
                second_file, second_vector = second_photo.name, second_photo.vectors[0]
                if pdist([first_vector, second_vector], 'euclidean') < EQUALITY_FACTOR:
                    person.add_photo(file_name=second_file, vector=second_vector)
                    to_remove.append(second_photo)

            for photo in to_remove:
                unclassified_photos.pop(photo)

            persons.append(person)

        logger.info(module=MODULE_NAME, message=f'{len(persons)} people recognized')

        return persons
