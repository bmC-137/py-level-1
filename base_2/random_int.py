import random


def gen_integer(min_, max_):
    random_int = int(random.randint(min_, max_))
    return random_int


b = gen_integer(1, 9999)
print(b)
