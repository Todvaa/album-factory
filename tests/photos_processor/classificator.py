import unittest

from dto import Photo
from photos_processor import classificators, recognizers


class ClassificatorTest(unittest.TestCase):
    def test_classification(self):
        photo_names = ['person1_1.png', 'person1_2.png', 'person2_1.png', 'person2_2.png', 'person3_1.png',
                       'person3_2.png']
        photos = [Photo(photo_name, '') for photo_name in photo_names]

        recognizer = recognizers.Recognizer('photos', photos)
        recognized_photos = recognizer.run()

        classificator = classificators.Classificator(recognized_photos)
        persons = classificator.run()
        self.assertEqual(3, len(persons))

        self.assertEqual(['person3_2.png', 'person3_1.png'], persons[0].photo_names)
        self.assertIsNotNone(persons[0].average_vector)

        self.assertEqual(['person2_2.png', 'person2_1.png'], persons[1].photo_names)
        self.assertIsNotNone(persons[1].average_vector)

        self.assertEqual(['person1_2.png', 'person1_1.png'], persons[2].photo_names)
        self.assertIsNotNone(persons[2].average_vector)


if __name__ == '__main__':
    unittest.main()
