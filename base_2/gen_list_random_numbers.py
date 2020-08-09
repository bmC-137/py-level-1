import random
from random import randrange

l = []


def gen_men_list():
	for i in range(1, 800):
		int_ = randrange(20)
		l.append(int_)


gen_men_list()
print(l, end='\n\n\n')



print('Test.2')
c = []
b = [c.append(random.randrange(20)) for i in range(100)]
print(c)

