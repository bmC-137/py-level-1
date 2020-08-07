import random


def generate_float(min_, max_):
    b = random.randint(min_, max_)
    r = random.randint(0, 99) / 100
    return b+r


c = generate_float(-180, 180)
print(c)
