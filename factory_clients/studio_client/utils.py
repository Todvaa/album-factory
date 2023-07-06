import random


def generate_random_code():
    return f'{random.randint(0, 999999):06d}'
