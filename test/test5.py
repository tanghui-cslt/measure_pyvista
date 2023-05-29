import pyvista as pv
import numpy as np

p = pv.Plotter(notebook=0)
# mesh = pv.Sphere()
mesh = pv.Cylinder().triangulate()
p.add_mesh(mesh,style="surface")
data = [0] * mesh.n_cells
actor_list = []
def callback(pos):
    p.add_text(f'{pos}', name='pos')
    # radius = 0.5
    # circle = pv.Circle(radius) 
    # p.add_mesh(circle, color='b')
    indices = mesh.find_containing_cell(pos)

    w = p.add_mesh(pv.Sphere(radius=0.03, center=pos),
                           color='red')
    
    print (indices)
    data[indices] = 1
    if indices  == -1:
        return 
    cell = mesh.get_cell(indices)
    n1 = cell.points[2]  -  cell.points[0]
    n2 = cell.points[1]  -  cell.points[0]
    normal_vector = np.cross(n1,n2)
    # mesh.cell_data['data'] =data
    # p.add_mesh(mesh)
    arc = pv.CircularArcFromNormal(pos, normal=normal_vector, angle=360)
    for i in actor_list:
        p.remove_actor(i)
    actor_list.clear()

    temp_actor = p.add_mesh(arc, color='g', line_width=2)
    actor_list.append(temp_actor)
# Tracks right clicks
p.track_click_position(callback=callback)
p.show()


# def clicked(event):
#     picker = pv._vtk.vtkPropPicker()
#     picker.PickProp(event[0], event[1],p.ren_win.GetRenderers().GetFirstRenderer())
#     actor=picker.GetActor()
#     if actor!=None:print(actor)
# p.track_click_position(callback=clicked,side='left', viewport=True) 
# p.show()



# import pyvista
# normal = [0, 0, 1]
# polar = [-1, 0, 0]
# arc = pv.CircularArcFromNormal([0, 0, 0], normal=normal, polar=polar,angle=90)
# pl = pv.Plotter()
# _ = pl.add_mesh(arc, color='k', line_width=10)
# _ = pl.show_bounds(location='all', font_size=30, use_2d=True)
# _ = pl.view_xy()
# pl.show()