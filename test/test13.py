import numpy as np
a = [1,2]
b = [3,4]
c = [a,b]
for [m,n] in c :
    if m in a :
        print('m',m)
    print(m,n)