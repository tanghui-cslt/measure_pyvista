import numpy as np
import pyvista as pv
from pyvista import examples
# def add(a):
#     a = a+3
# a = 5
# add(a)
# print(a)
# a = [1,2]
# b = []
# b.append(a)
# a = []
# print(a,b)


# c = np.array([1,2,3])
# d = np.array([4,5,6])

# e = np.hstack((c,d))
# print(e)
# # print(hash(e))
# f = set(e)
# print(f)

# mesh = examples.download_bunny()
# edges = mesh.extract_feature_edges(
#     boundary_edges=True, feature_edges=False, manifold_edges=False)

# p = pv.Plotter()
# p.add_mesh(mesh, color=True)
# p.add_mesh(edges, color="red", line_width=5)
# print(edges)
# print(edges.n_cells)
# edge_list = []
# for i in range(edges.n_cells):
#     edge = edges.get_cell(i)
#     edge_list.append(edge)
#     print(edge)


# for edge in edges.cell:
#     print(edge.point_ids)
# p.camera_position = [(-0.2, -0.13, 0.12), (-0.015, 0.10, -0.0), (0.28, 0.26, 0.9)]
# p.show()


# a =np.array([-1.35451030e-04,  3.11242034e-05,  1.50049996e+00])
# b = 1
# c = np.array([-1.35451030e-04,  -3.11242034e-05,  -1.50049996e+00])
# d = 2
# a1 = [a,b]
# c1 = [c,d]
# d1 = [a1,c1]
# def _find_elementId_from_list(single_list,list_data):
#         #查找多维list的元素的id,如果直接用in 某个list是否在另一个
#         # list里面,会出问题
#         len_single_data = len(single_list)
#         print("s= ", single_list)
#         print("ls= ", list_data)
#         for i,data in zip(range(len(list_data)), list_data):
#             print("data=",i,data)
#             list_flag = isinstance(data,list)
            
#             len_data = len(data)
#             if len_single_data == len_data:
#                 num = 0
#                 for j in range(len_data):
#                     list_flag = isinstance(data[j],np.ndarray)
#                     if list_flag:
#                         print("if_single_list",data[j])
#                         print (single_list[j])
#                         if (single_list[j] == data[j] ).all():
#                             num += 1 
#                     else:
#                         print("else_single_list",data[j])
#                         if (single_list[j] == data[j] ):
#                             num += 1 
#                 if num ==  len_data:
#                     return i
#                 else :
#                     print("num = ", num ,)
#                     # return -2
#             else:
#                 return -1
# id = _find_elementId_from_list(c1,d1)
# print(id )
# # print((c == d).any())
# # del a[0:2]
# # print(a)

# a = np.arange(1,7).reshape((2,3))
# b = np.arange(7,13).reshape((2,3))
# c = np.arange(13,19).reshape((2,3))
# print(a)
# print(b)
# print(c)

# a = np.vstack((a,b,c))
# print(a)
a =np.array( [ 3, -2,-3] )
b= np.array( [ 3,  2, -3] )
c= np.array( [ 2,  3, -3])
l  =  (a==b).all()
m  =  (a==c).all()
n  =  (c==b).all()
print(l,m,n)
import math 
a = np.arccos(0)

print(a/math.pi*180)