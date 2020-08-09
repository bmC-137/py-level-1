import random
from random import randrange
from pprint import pprint
from typing import Dict

c= []
b = [c.append(random.randrange(20)) for i in range(100)]


print('Test.1 with counter')
def most_frequent(List):
    counter = 0
    num = List[0]
    print('Printing num: ', num)

    for i in List:
        print('element:',i, end=' ')
        curr_frequency = List.count(i)
        print('frequency:',curr_frequency, end='\n')
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

d: Dict[int, int] = {}
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

# def most_frequent1(List):
#     return max(set(List), key=List.count)

print('Max Value is: ', max(set(c), key=c.count), end='\n\n\n\n')
# print(most_frequent(c),)
