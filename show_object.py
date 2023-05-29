import pyvista as pv
import numpy as np
import os, sys
from pyvista import examples,_vtk
from pyvista.utilities import check_valid_vector
# from pyvista.utilities.arrays import _coerce_pointslike_arg
# from pv import _vtk

def _select_object(parent,i):
    parent.plotter.clear()
    if i == 0:
        # os.path.join(dir_path, 'nut.ply')
        parent.mesh =pv.Cylinder(center=[1, 2, 3], direction=[1, 1, 1],
                            radius=1, height=2).triangulate()
        parent.plotter.add_mesh(parent.mesh,style='surface', show_edges=True,pickable=True)
        parent.mesh1 =examples.download_bunny_coarse().triangulate()
        parent.plotter.add_mesh(parent.mesh1,style='surface', show_edges=True,pickable=True)
        
    elif i == 1:
      
        parent.mesh =pv.Cylinder(center=[1, 2, 3], direction=[1, 1, 1],
                            radius=1, height=2).triangulate()
        parent.plotter.add_mesh(parent.mesh,style='surface', show_edges=True,pickable=True)

    elif i == 2:
        parent.mesh =examples.download_bunny_coarse().triangulate()
        parent.plotter.add_mesh(parent.mesh,style='surface', show_edges=True,pickable=True,color="white")
    
    elif i == 3:
        parent.mesh = examples.load_Cylinder()
        edges = parent.mesh.extract_feature_edges()
        # grid =examples.load_hexbeam()
        # parent.mesh = grid.extract_surface()
        # parent.mesh = pv.PolyData(examples.antfile)
        parent.plotter.add_mesh(parent.mesh,style='surface', show_edges=True,pickable=True)
        parent.plotter.add_mesh(edges, color="b")
        # print("------------------")
    parent.mesh=parent.mesh.compute_normals()
    parent.clear_all()
    # _traverse_point(parent)

def _show_bounds(parent):

    parent.bound_flag = not parent.bound_flag 
    if parent.bound_flag:
        parent.plotter.show_bounds(
            grid='front',
            location='outer',
            all_edges=True,
        )

    else:
            parent.plotter.remove_bounds_axes()
            parent.plotter.remove_bounding_box()
    # print("test+",parent.bound_flag)
    
def _wire_surface(parent,actor_list):
    parent.plotter.clear()
    for actor in actor_list:
        for single_actor in actor:
            parent.plotter.remove_actor(single_actor)

    for actor in actor_list:
        for single_actor in actor:
            parent.plotter.add_actor(single_actor)
    
    if(parent.flag_wire_surface):
        parent.plotter.add_mesh(parent.mesh,style='wireframe', show_edges=True,pickable=True)
    else:
        print("-----")
        parent.plotter.add_mesh(parent.mesh,style='surface', show_edges=True,pickable=True)

    parent.flag_wire_surface = not parent.flag_wire_surface
    # print("flag = ",parent.flag_wire_surface )
    
def _traverse_point(parent):
    print(parent.mesh.points)

def _clear_data(parent):
    parent.clear_left_data(parent.label1)
    parent.clear_right_data(parent.label2)

    parent.clear_left_data(parent.label)
    parent.clear_right_data(parent.label_2)