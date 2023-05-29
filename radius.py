import numpy as np 
import pyvista as pv
import distance 
import find_cylinder
# actor_list = []
class Picker_circle:
    def __init__(parent, plotter, mesh, circleLabel,radius_actor):
        parent.plotter = plotter
        parent.mesh = mesh
        parent._points = []
        # parent.actor_list = []
        parent.label = circleLabel
        parent.radius_actor = radius_actor
        # if 'Normals' not in parent.mesh.cell_data.keys():
            # parent.mesh=parent.mesh.compute_normals()
    
    @property
    def points(parent):
        """To access all th points when done."""
        return parent._points
    
    def  _calc_radius_from_three_points(parent,indices):
        cell = parent.mesh.get_cell(indices)
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
    
    def _is_a_point_on_circle(parent,center,R,i,points,origin_indices):
        cell = parent.mesh.get_cell(i)
        
        num = 0
        for point in cell.points:
            if point  in points:
                continue

            R1 = np.linalg.norm(np.array(point-center))
            if abs(R1-R)<1e-6:
                # indices = parent.mesh.find_containing_cell(point)
                # temp_cell = parent.mesh.get_cell(indices)
                # print("point ==== ", point,indices,origin_indices,abs(R1-R))

                num = 1
        return num

    def __call__(parent, *args):
        
        picked_pt = np.array(parent.plotter.pick_mouse_position())
        direction = picked_pt - parent.plotter.camera_position[0]
        direction = direction / np.linalg.norm(direction)
        start = picked_pt - 1000 * direction
        end = picked_pt + 10000 * direction
        point, ix = parent.mesh.ray_trace(start, end, first_point=True)
        if len(point) > 0:
            indices = parent.mesh.find_containing_cell(point)
            # parent._points.append(point)
            # parent.mesh
            points = parent.mesh.bounds
            interval = 100
            x = abs(points[1]-points[0])/interval
            y = abs(points[3]-points[2])/interval
            z = abs(points[5]-points[4])/interval
            radius = (x+y+z)/10
            point_actor = parent.plotter.add_mesh(
                pv.Sphere(radius=radius, center=point),color='red', reset_camera=False)
            
            print ("ind = ",indices)

            if indices == -1:
                
                parent.plotter.remove_actor(point_actor)
                return
            
            [center,polar,R]=parent._calc_radius_from_three_points(indices) 

            origin_cell = parent.mesh.get_cell(indices)

            normals = parent.mesh.cell_data['Normals']
            normal_vector1 = normals[indices]
            differences = np.linalg.norm(normals-normal_vector1,axis=1)
            # print("diff = ", differences)
            parent.mesh.cell_data["scalars"]=differences 
            
            unstructGrid_threshed = parent.mesh.threshold(value=1e-4,invert=True)
            
            cell_threshed = unstructGrid_threshed.cells
            num = 0
            for i in cell_threshed:
                # cell = parent.mesh.get_cell(i)
                num += parent._is_a_point_on_circle(center,R,i,origin_cell.points,origin_indices=indices)

            arc = pv.CircularArcFromNormal(center,resolution=100,polar=polar, 
                                           normal=normal_vector1, angle=360)

            print("num=",num,len(cell_threshed))
            circle_actor = parent.plotter.add_mesh(arc,
                 color='g', line_width=4, reset_camera=False,)
            if num < 3:
                # for i in actor_list:
                #     parent.plotter.remove_actor(i)
                for i in parent.radius_actor:
                    parent.plotter.remove_actor(i)
                # parent.plotter.remove_actor(point_actor)
                parent.radius_actor.clear()
                parent.plotter.remove_actor(circle_actor)
                parent.radius_actor.append(point_actor)
                # actor_list.append(point_actor)
                parent.label.setText("")
                # parent.plotter.remove_actor(threshed_actor)
                return 
            
            else: 
                for i in parent.radius_actor:
                    parent.plotter.remove_actor(i)

                str1 = "Center ="+str(center)+"\n"
                str2 = "Radius ="+str(R)+"\n"
                str3 = "Diameter ="+str(2*R)+"\n"
                str4 = str1 + str2 + str3
                parent.label.setText(str4)
                parent.radius_actor.clear()

                parent.radius_actor.append(circle_actor)
                parent.radius_actor.append(point_actor)
                # actor_list.append(threshed_actor)

            
        return
    
class Picker_cylinder:
    def __init__(parent, plotter, 
        mesh, cylinderLabel,radius_actor,left_point,right_point):
        parent.plotter = plotter
        parent.mesh = mesh
        parent._points = []
        # parent.actor_list = []
        parent.label = cylinderLabel
        parent.radius_actor = radius_actor
        parent.left_point = left_point
        parent.right_point = right_point
        # if 'Normals' not in parent.mesh.cell_data.keys():
            # parent.mesh=parent.mesh.compute_normals()

    def _find_closet_cylinder_to_cell(parent,cylinder_list,index):
        cell = parent.mesh.get_cell(index)
        for point in cell.points:
            for circle_list  in cylinder_list:
                for edge in circle_list :
                    pass

    def _show_cylinder(parent,cylinder_list):
        color = ['r','g','b','y']
        num = 0
        for circle in cylinder_list:
            # origin_circle = circle[0]
            j = 0
            center_list = []
            len_circle = len(circle)
            if(len_circle ==1 ):
                continue
            for single_circle in circle:
                center_list.append(single_circle[0])
                arc = pv.CircularArcFromNormal(single_circle[0],
                resolution=100,polar=single_circle[1],
                normal=single_circle[3], angle=360)
                circle_actor = parent.p.add_mesh(arc,
                color=color[num], line_width=4, 
                reset_camera=False,show_edges = True)
                if (j==1):
                    lien_actor = parent.p.add_lines(
                        np.array(center_list),color=color[num])
                    parent.radius_actor.append(lien_actor)
                # print("R = ",single_circle[2])
                j += 1
                parent.radius_actor.append(circle_actor)
            num += 1


    def __call__(parent, *args):
        for actor in parent.radius_actor:
            parent.plotter.remove_actor(actor)
        fv = find_cylinder.Find_Cylinder(parent.plotter,parent.mesh)
        # cylinder_list includes all cylinders 
        cylinder_list = fv.find_cylinder()

        picked_pt = np.array(parent.plotter.pick_mouse_position())
        direction = picked_pt - parent.plotter.camera_position[0]
        direction = direction / np.linalg.norm(direction)
        start = picked_pt - 1000 * direction
        end = picked_pt + 10000 * direction
        point, ix = parent.mesh.ray_trace(start, end, first_point=True)
        if len(point) > 0:
            indices = parent.mesh.find_containing_cell(point)
            # parent._points.append(point)
            # parent.mesh
            points = parent.mesh.bounds
            interval = 100
            x = abs(points[1]-points[0])/interval
            y = abs(points[3]-points[2])/interval
            z = abs(points[5]-points[4])/interval
            radius = (x+y+z)/10
            point_actor = parent.plotter.add_mesh(
                pv.Sphere(radius=radius, center=point),
                color='red', reset_camera=False)
            
            if indices == -1:
                
                parent.plotter.remove_actor(point_actor)
                return
            

        # parent._show_cylinder(cylinder_list)
        # actors = parent.plotter.renderer.actors
        # print("test", actors)
       