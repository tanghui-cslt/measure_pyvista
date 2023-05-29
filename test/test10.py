import numpy as np

def f(x,y):
    return 10*x+y
a = np.fromfunction(f,(5,4),dtype=int)
print(a)
b = [2,4]
c = a[b,:]
print(c)
