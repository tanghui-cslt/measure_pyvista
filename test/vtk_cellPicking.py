#!/usr/bin/env python

# noinspection PyUnresolvedReferences
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


# Catch mouse events


class MouseInteractorStyle(vtkInteractorStyleTrackballCamera):
    def __init__(self, data):
        # self.AddObserver('LeftButtonPressEvent', self.left_button_press_event)
        # self.AddObserver('LeftButtonPressEvent', self.left_button_press_event)
        self.key_press = self.AddObserver(_vtk.vtkCommand.KeyPressEvent, self.key_press_event)
        
        # self.point_picker.AddObserver(_vtk.vtkCommand.EndPickEvent, self.test)
        # self.AddObserver(vtk.vtkCommand.EndPickEvent, self.left_button_press_event)
        self.data = data
        self.selected_mapper = vtkDataSetMapper()
        self.selected_actor = vtkActor()
    def key_press_event(self,picker,event):
        Interactor = self.GetInteractor()
        keySym = Interactor.GetKeySym()
        
        if keySym in ['p', 'P']:
            self.left_button_press_event(picker,event)
            print("p is pushed")
    
        print("key = ")

    def test(self,picker, event):
        picked_point_id = picker.GetPointId()
        print("point = ", picked_point_id)
        if  (picked_point_id < 0):
            return None
        self._picked_point = np.array(picker.GetPickPosition())
        self._picked_mesh = picker.GetDataSet()
        print("test-point picker",event, self._picked_point)

    def enable_triangle(self,obj,event):
        self.point_picker = _vtk.vtkPointPicker()
        self.point_picker.SetTolerance(0.5)
        pass 

    def left_button_press_event(self, obj, event):
        colors = vtkNamedColors()

        # Get the location of the click (in window coordinates)
        pos = self.GetInteractor().GetEventPosition()

        picker = vtkCellPicker()
        picker.SetTolerance(0.0005)

        # Pick from this location.
        picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        world_position = picker.GetPickPosition()
        print(f'Cell id is: {picker.GetCellId()}')

        if picker.GetCellId() != -1:
            print(f'Pick position is: ({world_position[0]:.6g}, {world_position[1]:.6g}, {world_position[2]:.6g})')

            ids = vtkIdTypeArray()
            ids.SetNumberOfComponents(1)
            ids.InsertNextValue(picker.GetCellId())

            selection_node = vtkSelectionNode()
            selection_node.SetFieldType(vtkSelectionNode.CELL)
            selection_node.SetContentType(vtkSelectionNode.INDICES)
            selection_node.SetSelectionList(ids)

            selection = vtkSelection()
            selection.AddNode(selection_node)

            extract_selection = vtkExtractSelection()
            extract_selection.SetInputData(0, self.data)
            extract_selection.SetInputData(1, selection)
            extract_selection.Update()

            # In selection
            selected = vtkUnstructuredGrid()
            selected.ShallowCopy(extract_selection.GetOutput())

            print(f'Number of points in the selection: {selected.GetNumberOfPoints()}')
            print(f'Number of cells in the selection : {selected.GetNumberOfCells()}')

            self.selected_mapper.SetInputData(selected)
            self.selected_actor.SetMapper(self.selected_mapper)
            self.selected_actor.GetProperty().EdgeVisibilityOn()
            self.selected_actor.GetProperty().SetColor(colors.GetColor3d('Tomato'))

            self.selected_actor.GetProperty().SetLineWidth(3)

            self.GetInteractor().GetRenderWindow().GetRenderers().GetFirstRenderer().AddActor(self.selected_actor)

        # Forward events
        self.OnLeftButtonDown()


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

    plane_source = vtkPlaneSource()
    plane_source.Update()

    triangle_filter = vtkTriangleFilter()
    triangle_filter.SetInputConnection(cylinderSource.GetOutputPort())
    # triangle_filter.SetInputConnection(plane_source.GetOutputPort())
    triangle_filter.Update()

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(triangle_filter.GetOutputPort())

    actor = vtkActor()
    actor.GetProperty().SetColor(colors.GetColor3d('SeaGreen'))
    actor.SetMapper(mapper)

    renderer = vtkRenderer()
    ren_win = vtkRenderWindow()
    ren_win.AddRenderer(renderer)
    ren_win.SetWindowName('CellPicking')
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)
    # renderer.GetActors().
    renderer.AddActor(actor)
    # renderer.ResetCamera()
    renderer.SetBackground(colors.GetColor3d('PaleTurquoise'))

    # Add the custom style.
    style = MouseInteractorStyle(triangle_filter.GetOutput())
    style.SetDefaultRenderer(renderer)
    iren.SetInteractorStyle(style)
    style.GetInteractor()
    style.GetCurrentRenderer()
    
    # iren.SetPicker(style.point_picker )

    ren_win.Render()
    iren.Initialize()
    iren.Start()


if __name__ == '__main__':
    import sys

    main(sys.argv)