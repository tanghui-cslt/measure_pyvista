import pyvista as pv
import numpy as np 
from pyvista import examples

# points = np.random.rand(100,3)
# mesh = pv.PolyData(points)
# mesh.plot(point_size = 5, style = 'points', color = 'tan')


# mesh = examples.load_hexbeam()

# pl = pv.Plotter()
# pl.add_mesh(mesh, show_edges=True, color='white')
# pl.add_points(mesh.points, color='red', point_size=20)

# single_cell = mesh.extract_cells(mesh.n_cells - 1)

# pl.add_mesh(single_cell, color='pink', edge_color='blue',
#             line_width=5, show_edges=True)


# cpos = [(6.20, 3.00, 7.50), (0.16, 0.13, 2.65), (-0.28, 0.94, -0.21)]
# pl.camera_position = cpos
# pl.show()


# mesh = examples.download_bunny_coarse()

# pl = pv.Plotter()
# pl.add_mesh(mesh, show_edges=True, color='white')
# pl.add_points(mesh.points, color='red', point_size=20)

# single_cell = mesh.extract_cells(mesh.n_cells - 1)
# pl.add_mesh(single_cell, color='pink', edge_color='blue',
#             line_width=5, show_edges=True)

# pl.camera_position = [(0.02, 0.30, 0.73),
#                       (0.02, 0.03, -0.022),
#                       (-0.03, 0.94, -0.34)]
# pl.show()


# mesh.point_data['my point values'] = np.arange(mesh.n_points)
# print(mesh.point_data['my point values'])
# mesh.plot(scalars='my point values', cpos = cpos, show_edges=True)

# mesh.cell_data['my cell values'] = np.arange(mesh.n_cells)
# print(mesh.cell_data['my cell values'])
# print(single_cell.n_cells)
# mesh.plot(scalars = 'my cell values', cpos = cpos, show_edges = True)

# uni = examples.load_uniform()
# mesh =examples.load_nut()
# p1 = pv.Plotter()
# p1.add_mesh(mesh, show_edges=True,pickable=True)

# # submehs = pv.Plotter.enable_horizon_picking()
# def path_callback(picked_path):
#     # len1 = len(picked_path)
#     print("----",picked_path)


# p1.enable_path_picking(callback=path_callback,
#                     line_width = 10,color='r',
#                                show_path =True)

# # p1.add_mesh(submehs, color='r')
# # p1.subplot(0,1)
# # p1.add_mesh(mesh, scalars='Spatial Cell Data', show_edges=True)
# p1.show()

def test_a(a,b):
    def add(a,b):
        return a+b
    c = add(a,b)
    return c

d = test_a(1,3)
test_a(1,3).add(2,3)
print(d)