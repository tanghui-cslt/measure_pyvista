import vtkmodules.vtkRenderingOpenGL2
import numpy as np
from pyvista import _vtk
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkIdTypeArray
from vtkmodules.vtkCommonDataModel import (
    vtkSelection,
    vtkSelectionNode,
    vtkUnstructuredGrid
)
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersExtraction import vtkExtractSelection
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
import pyvista as pv

class KeyboardInteractorStyle(vtkInteractorStyleTrackballCamera):

    def __init__(self, data):
        # self.AddObserver('LeftButtonPressEvent', self.left_button_press_event)
        # self.AddObserver('LeftButtonPressEvent', self.left_button_press_event)
        self.key_press = self.AddObserver(_vtk.vtkCommand.KeyPressEvent, self.key_press_event)
    def key_press_event(self,obj,event):
        pass 
    def enable_cell(self,tolerance=0.0001):
        pass 

def main(argv):
    colors = vtkNamedColors()
    center=[1, 2, 3]
    direction=[1, 1, 1]
    radius=1
    height=2
    resolution=100
    capping=True
    cylinderSource = _vtk.vtkCylinderSource()
    cylinderSource.SetRadius(radius)
    cylinderSource.SetHeight(height)
    cylinderSource.SetCapping(capping)
    cylinderSource.SetResolution(resolution)
    cylinderSource.Update()

    mesh =pv.Cylinder(center=[1, 2, 3], direction=[1, 1, 1],
                            radius=1, height=2).triangulate()
    style = KeyboardInteractorStyle(mesh)
    


if __name__ == '__main__':
    import sys

    main(sys.argv)