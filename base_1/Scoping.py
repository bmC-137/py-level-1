#!/usr/bin/python3

# adding x here makes it in scope
x = 0

for i in range(1,25):
    #  x is in scope
    x = i + x

# x is now out of scope
print(x)

