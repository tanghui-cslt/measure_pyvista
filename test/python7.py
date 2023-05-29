# import pyvista as pv
# from pyvista import examples
# # grid = pv.Cylinder().triangulate()
# # cell = grid.extract_cells(31)  
# # ind = grid.neighbors(31)  
# # neighbors = grid.extract_cells(ind)  

# # plotter = pv.Plotter()
# # plotter.add_axes()  
# # plotter.add_mesh(cell, color='r', show_edges=True)  
# # plotter.add_mesh(neighbors, color='b', show_edges=True)  
# # plotter.show()

# grid = pv.Cylinder().triangulate()
# grid = grid.compute_connectivity()  
# grid.plot(show_edges=True)  
# a= [1,2]
# c = [[1,2],[1,3]]
# if a in c:
#     print(1111)
# else:
#     print(222)

# import pyvista
# import numpy as np
# mesh = pyvista.Cube()
# c =[mesh.n_points - a for a in np.arange(mesh.n_points)]
# mesh.point_data['data0'] = c
# print("c = ",c)
# print("test = ",mesh.point_data.active_scalars)

# mesh.point_data['data1'] = np.arange(mesh.n_points)
# print(mesh.point_data.active_scalars)

from pathlib import Path
from vtkmodules.vtkIOGeometry import (
    vtkBYUReader,
    vtkOBJReader,
    vtkSTLReader
)
import vtkmodules.vtkInteractionStyle
import sys,os
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.vtkCommonColor import vtkNamedColors
import vtkmodules.vtkRenderingOpenGL2

dir_path = "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\Lib\\site-packages\\pyvista\\examples"

def ReadPolyData(file_name):
    valid_suffixes = ['.g', '.obj', '.stl', '.ply', '.vtk', '.vtp']
    path = Path(file_name)
    if path.suffix:
        ext = path.suffix.lower()
    if path.suffix not in valid_suffixes:
        print(f'No reader for this file suffix: {ext}')
        return None
    else:
        if ext == ".ply":
            print("-------0-")
            reader = vtkPLYReader()
            reader.SetFileName(file_name)
            reader.Update()
            poly_data = reader.GetOutput()
            return poly_data

path = os.path.join(dir_path, 'nut.ply')
print(path)
poly_data = ReadPolyData(path)
# print(poly_data)

colors = vtkNamedColors()
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(poly_data)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(colors.GetColor3d('Tan'))

ren = vtkRenderer()
renWin = vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('ReadPLY')

iren = vtkRenderWindowInteractor()
ren.SetRenderWindow(renWin)

ren.AddActor(actor)

iren.Initialize()
renWin.Render()

ren.SetBackground(colors.GetColor3d('AliceBlue'))
ren.GetActiveCamera().SetPosition(-0.5, 0.1, 0.0)
ren.GetActiveCamera().SetViewUp(0.1, 0.0, 1.0)
renWin.Render()
iren.Start()