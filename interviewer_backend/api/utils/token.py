import random
import string


def random_string(length: int = 32):
    return "".join([random.choice(string.ascii_letters) for _ in range(length)])


def random_int(length: int = 6):
    return random.randint(10 ** (length - 1), 10**length - 1) if length > 0 else 0
