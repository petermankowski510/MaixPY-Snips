# uheapq - By: TIUser - Thu May 7 2020

import uheapq as q

"""Heap elements can be tuples. This is useful for assigning comparison values
such as task priorities alongside the main record being tracked """
a=(7, 'one')
b=(1, 'two')
c=(6, 'thr')
d=(3, 'for')

h = []
q.heappush(h, a)
q.heappush(h, b)
q.heappush(h, c)
q.heappush(h, d)


for i in range(0, 4):
    print(q.heappop(h))

# Python program to demonstrate
# accessing a element from a Dictionary
name = ['o', 'p', 'c']
roll = [3,5,7]
id = [12,13,14]

# Creating a Dictionary
Dict = zip(name, roll, id)

# converting values to print as set
Dict = set(Dict)

print(Dict)

# unzipping values
a,b,c = zip(*Dict)

print(a , b, c)

