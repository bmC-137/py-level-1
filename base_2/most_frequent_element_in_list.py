import random
from random import randrange

c= []
b = [c.append(random.randrange(20)) for i in range(100)]


print('Test.1 with counter')
def most_frequent(List):
    counter = 0
    num = List[0]
    print('Printing num: ', num)

    for i in List:
        print('Printing list element: ', i)
        curr_frequency = List.count(i)
        print('Priting element frequency: ', curr_frequency)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num


a = most_frequent(c)

print('Most is: ', a, end='\n\n\n\n')
