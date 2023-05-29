import sys
import numpy as np
a = 1
b = 3
np_vector1 = np.array([0,0,0])
np_vector2 = np.array([2,0,0])
np_vector3 = np.array([1,5,0])

np1 = np_vector2 - np_vector1
np2 = np_vector3 - np_vector1
np3 = np.cross(np1,np2)

area = np.linalg.norm(np3)
edge_lenght = np.linalg.norm(np1)
height = area/edge_lenght
print("height = " + str(height))
if a==1 and b==3:
    print("test")