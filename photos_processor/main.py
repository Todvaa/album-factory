from photos_processor.classificators import Classificator
from photos_processor.recognizers import Recognizer


def run():
    # local_path = download_photos()
    # recognizer = Recognizer(local_path)
    recognizer = Recognizer('test_photos')
    persons_vectors = recognizer.run()
    classificator = Classificator(persons_vectors)
    classificator.run()


if __name__ == "__main__":
    run()
