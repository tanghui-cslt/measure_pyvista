import numpy as np
import pyvista
import pyvista as pv
from pyvista import examples

# cent = np.random.random((10, 3))
# direction = np.random.random((10, 3))
# plotter = pyvista.Plotter()
# _ = plotter.add_arrows(cent, direction, mag=2)
# plotter.show()

# sphere = pyvista.Sphere()
# plotter = pyvista.Plotter()
# _ = plotter.add_mesh(sphere)
# _ = plotter.add_cursor()
# plotter.show()

_orientation = np.array([])
print(len(_orientation))
rotate = [0]*1
rotate[0] = [0]*4
a = (3,4,5)
b = np.array(a)
print('rotate = ',rotate,a,b)
# Whole bunch of lines that make a mesh
mesh = examples.download_bunny_coarse().triangulate()
# self.plotter.add_mesh(self.sphere,style='wireframe', show_edges=True,pickable=True) 
p = pv.Plotter(notebook=False)
# p.add_mesh(mesh,style='surface',pickable=True)
p.add_mesh(mesh,style='wireframe',pickable=True)
p.enable_cell_picking(through=False,color='r')
# p.add_points(mesh.points, pickable=False, color="red", render_points_as_spheres=True)
p.show()

# plane = pv.Plane(i_size=1.5, j_size=1.5)
# mesh=pv.Sphere().clip_surface(plane, invert=False)
# p1=pv.Plotter()
# actor = p1.add_mesh(mesh, smooth_shading=True)
# actor.prop.color='r'
# actor.backface_prop.color='lightbule'
# _=p1.add_mesh(
#     plane, opacity=0.25, show_edges=True, color='grey',lighting=False
# )
# p1.show()


# v = np.array([[0,0,0], [1,1,1], [2,2,2], [3,3,3], [0,1,2], [0,2,4]]).astype('float')
# lines =[4, 0, 1, 2, 3, 3, 0, 4, 5]

# pl = pv.Plotter()
# mesh = pv.PolyData(var_inp=v, lines=lines, n_lines=2)
# pl.add_mesh(mesh, pickable=True)
# pl.enable_cell_picking(through=True, color='r')
# pl.show()