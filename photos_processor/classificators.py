from abc import ABC, abstractmethod

from scipy.spatial.distance import pdist

from photos_processor.constants import EQUALITY_FACTOR, MODULE_NAME
from photos_processor.dto import Person
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
            first_s3_path, first_vector = first_photo.remote_url, first_photo.vectors[0]
            person = Person(photo_s3_path=first_s3_path, vector=first_vector)
            to_remove = []
            for index, second_photo in enumerate(unclassified_photos):
                second_s3_path, second_vector = second_photo.remote_url, second_photo.vectors[0]
                if pdist([first_vector, second_vector], 'euclidean') < EQUALITY_FACTOR:
                    person.add_photo(photo_s3_path=second_s3_path, vector=second_vector)
                    to_remove.append(index)

            for index in reversed(to_remove):
                unclassified_photos.pop(index)

            persons.append(person)

        logger.info(module=MODULE_NAME, message=f'{len(persons)} people recognized')

        return persons
