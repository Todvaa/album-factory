from photos_processor.classificators import Classificator
from photos_processor.recognizers import Recognizer


def run():
    # local_path = download_photos()
    # recognizer = Recognizer(local_path)
    recognizer = Recognizer('test_photos')
    persons_vectors = recognizer.run()
    classificator = Classificator(persons_vectors)
    persons = classificator.run()
    # todo: сделать слушателя = консьюмер photos_procesfasfaing
    # todo: положить в photos_prsdgsdgsed [persons_vectors, persons]

if __name__ == "__main__":
    run()
