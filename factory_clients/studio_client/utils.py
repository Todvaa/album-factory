from random import randint


def generate_random_code():
    return f'{randint(0, 999999):06d}'
