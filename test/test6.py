import pyvista as pv
from pyvista import examples
import numpy as np
import math 
from pyvista.utilities.arrays import _coerce_pointslike_arg
from pyvista import _vtk
import vtk
class Picker:
    def __init__(self, plotter, mesh):
        self.plotter = plotter
        self.mesh = mesh
        self._points = []
        self.actor_list = []
        
    @property
    def points(self):
        """To access all th points when done."""
        return self._points
    def  _calc_circle_radius(self,indices):
        cell = self.mesh.get_cell(indices)
        
        A = np.array(cell.points[0])
        B = np.array(cell.points[1])
        C = np.array(cell.points[2])
        a = np.linalg.norm(C - B)
        b = np.linalg.norm(C - A)
        c = np.linalg.norm(B - A)
        s = (a + b + c) / 2
        R = a*b*c / 4 / np.sqrt(s * (s - a) * (s - b) * (s - c))
        b1 = a*a * (b*b + c*c - a*a)
        b2 = b*b * (a*a + c*c - b*b)
        b3 = c*c * (a*a + b*b - c*c)
        center = np.column_stack((A, B, C)).dot(np.hstack((b1, b2, b3)))
        center /= b1 + b2 + b3

        polar = center-cell.points[2] 

        return center,polar,R
    def _traverse_mesh(self,center,R,indices):
        cell = mesh.get_cell(indices)
        # for point in cell.points:
            # cell_array = self.mesh.find_containing_cell(point)
            # point, singular = _coerce_pointslike_arg(point, copy=False)
            # locator = _vtk.vtkCellLocator()
            # locator.SetDataSet(mesh.GetOu)
            # locator.BuildLocator()

            # containing_cells = [locator.FindCell(node) for node in point]
            # print("fasd:",containing_cells)
            # print("cell_array=", cell_array,point,cell_array.shape)


    def __call__(self, *args):
        picked_pt = np.array(self.plotter.pick_mouse_position())
        direction = picked_pt - self.plotter.camera_position[0]
        direction = direction / np.linalg.norm(direction)
        start = picked_pt - 1000 * direction
        end = picked_pt + 10000 * direction
        point, ix = self.mesh.ray_trace(start, end, first_point=True)
        if len(point) > 0:
            indices = self.mesh.find_containing_cell(point)
            # self._points.append(point)
            circle_actor = p.add_mesh(pv.Sphere(radius=0.003, center=point),
                           color='red')
            print ("ind = ",indices)
            if indices == -1:
                return
            normal_vector1 = mesh.cell_data['Normals'][indices]
            [center,polar,R]=self._calc_circle_radius(indices) 
            self._traverse_mesh(center,R,indices)
            
            #judge if the center is on surface
            center_indices = self.mesh.find_containing_cell(center)
            print("center=",center_indices)
            if center_indices == -1:
                return 

            arc = pv.CircularArcFromNormal(center,resolution=100,polar=polar, normal=normal_vector1, angle=360)
           
            for i in self.actor_list:
                p.remove_actor(i)

            self.actor_list.clear()
            temp_actor = p.add_mesh(arc, color='g', line_width=4)

            self.actor_list.append(temp_actor)

            self.actor_list.append(circle_actor)
        return


# mesh = examples.load_airplane()
# polygonSource = vtk.vtkRegularPolygonSource()
# polygonSource.GeneratePolygonOff()
# polygonSource.SetNumberOfSides(50)
# polygonSource.SetRadius(5.0)
# polygonSource.SetCenter(0.0, 0.0, 0.0)
# polygonSource.Update()
mesh = pv.Cylinder().triangulate()
# mesh = pv.wrap(polygonSource.GetOutput)
# mesh = pv.Sphere().triangulate()
p = pv.Plotter(notebook=False)
p.add_mesh(mesh, style="surface",show_edges=True, color='w')

picker = Picker(p, mesh)

mesh=mesh.compute_normals()
p.track_click_position(picker, side='right')
p.add_text('Use right mouse click to pick points')

p.show()