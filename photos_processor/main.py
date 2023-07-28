def run():
    local_path = dowload_photos()
    recognizer = new
    Recognizer(local_path)
    persons_vectors = recognizer.run()


if __name__ == "__main__":
    run()
