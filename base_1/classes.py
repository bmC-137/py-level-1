#!/usr/bin/python

class me:
    def __init__(self, foo):
        self.myvar = foo

    def getval(self):
        return self.myvar

my = me("this")
x = my.getval()
print(x)
