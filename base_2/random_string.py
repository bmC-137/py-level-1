import random
import string


# Var. 1
def get_random_string(size):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(size))
    print("random string is: ", result_str, end='\n')
    return result_str

i = get_random_string(15)
print('Type is: ', type(i), i, end='\n')




# Var. 2
def get_string(size):
    str_pool = [x for x in string.ascii_lowercase + string.ascii_uppercase]
    m = to_int(size)
    s = []
    for i in range(m):
        y = random.randint(0, len(str_pool) - 1)
        s.append(str_pool[y])
    return ''.join(s)

def to_int(num_):
    try:
        v = int(num_)
        return v
    except (ValueError, TypeError):
        print('error')
        return 0

b=get_string(9)
print(b)
