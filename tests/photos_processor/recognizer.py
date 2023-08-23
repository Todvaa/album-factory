import unittest

import recognizers
from dto import Photo


class RecognizerTest(unittest.TestCase):
    def test_face_vector(self):
        recognizer = recognizers.Recognizer('photos', [Photo('person1_1.png', '')])
        photos = recognizer.run()
        self.assertEqual(128, len(photos[0].vectors[0]))

    def test_face(self):
        photo_names = ['person1_1.png', 'person1_2.png', 'person2_1.png', 'person2_2.png', 'person3_1.png',
                       'person3_2.png']
        photos = [Photo(photo_name, '') for photo_name in photo_names]

        recognizer = recognizers.Recognizer('photos', photos)
        recognized_photos = recognizer.run()
        self.assertEqual(6, len(recognized_photos))
        for recognized_photo in recognized_photos:
            self.assertEqual(1, recognized_photo.face_count)
            self.assertEqual(1, len(recognized_photo.vectors))

    # def test_group_face(self):
    #     photo_names = ['group.png']
    #     photos = [Photo(photo_name, '') for photo_name in photo_names]
    #
    #     recognizer = recognizers.Recognizer('photos', photos)
    #     recognized_photos = recognizer.run()
    #     self.assertEqual(1, len(recognized_photos))
    #     self.assertEqual(5, recognized_photos[0].face_count)
    #     self.assertEqual(5, len(recognized_photos[0].vectors))

    def test_non_face(self):
        recognizer = recognizers.Recognizer('photos', [Photo('non_face.jpeg', '')])
        photos = recognizer.run()
        self.assertEqual(0, len(photos))


if __name__ == '__main__':
    unittest.main()
