import random
from random import randrange
from pprint import pprint

c = []
b = [c.append(random.randrange(20)) for i in range(100)]

print('Test.1 with counter')


def most_frequent(List):
	counter = 0
	num = List[0]
	print('Printing num: ', num)

	for i in List:
		print('element:', i, end=' ')
		curr_frequency = List.count(i)
		print('frequency:', curr_frequency, end='\n')
		if (curr_frequency > counter):
			counter = curr_frequency
			num = i

	return num


a = most_frequent(c)

print('Most is: ', a, end='\n\n\n\n')
###
###
###
print('Test.2 with dictionary and \"count\" method with max')

d = {}
for i in c:
	d[i] = c.count(i)
# adding some sort to dictionary.
print(dict(sorted(d.items())))
print('Max Value is: ', max(d.keys(), key=d.get), end='\n\n\n\n')
'''
Explanation:
max(d, key=d.get) => Gets the key with the maximum value where d is the dictionary
d.get => gets the value associated with that key
'''
##
##
##
##

print('Test.3 with set and list and max')
# seems not very accurate.... like test 1
# def most_frequent1(List):
#     return max(set(List), key=List.count)
print('Max Value is: ', max(set(c), key=c.count), end='\n\n\n\n')
##
##
##
##

print('Test.4 with counter from collections')
from collections import Counter


def most_freq(l_):
	occurence_count = Counter(l_)
	return occurence_count.most_common(1)


b_ = most_freq(c)
for key, value in b_:
	print('Most Freq:', key, 'wich repeated:', value, end='\n\n\n\n\n')


##
##
##
##

print('Test.5 with finding mode from statistics')
import statistics
from statistics import mode

def most_common(ll):
	return mode(ll)

print(most_common(c))

