import pyvista  as pv
import numpy as np
from pyvista import _vtk
from pyvista.utilities import try_callback
def _pick_line(parent,    
        callback=None,
        show_message=False,
        font_size=18,
        color='pink',
        point_size=10,
        line_width=5,
        show_path=True,
        tolerance=0.025,
        side ='left',
        label = None,
        # right_label= None,
        **kwargs,
):
    
    def make_line_cells(n_points):
        cells = np.arange(0, n_points, dtype=np.int_)
        cells = np.insert(cells, 0, n_points)
        return cells

    # the_points = []
    # the_ids = []
    def _the_callback(mesh, idx):
        if mesh is None:
            return
        points = mesh.points[idx]
        if side == 'left':
            # label = left_label
            parent.left_line_points.append(points)
            the_points = parent.left_line_points
        elif side == 'right':
            # label = right_label
            parent.right_line_points.append(points)
            the_points = parent.right_line_points
 
        len_point = len(the_points)
        if len_point >2:
            str1 = label.text()
            str2 = "\nError, you have selected a line!\n"
            label.setText(str1+str2)

            return 
        
        elif len_point == 2:
            picked_path = pv.PolyData(np.array(the_points))
            picked_path.lines = make_line_cells(len(the_points))
            
            line_actor = parent.plotter.add_mesh(
                        picked_path,
                        color=color,
                        line_width=line_width,
                        point_size=point_size,
                        reset_camera=False,
                        **kwargs,
                    )
            str1 = "Selected points:"+str(len_point)
            str2 = str1 + "\n" + "Coordinates of points:" +str(the_points)
            if side == 'left':
                for point in the_points:
                    parent.left_point.append(point)
                parent.left_line_actor.append(line_actor)

            elif side == 'right':

                for point in the_points:
                    parent.right_point.append(point)
                parent.right_line_actor.append(line_actor)

            label.setText(str2)
            if callable(callback):
                try_callback(callback,parent)
        else :
            # parent.label1.setText("Selected points:"+str(len_point))
            str1 = "Selected points:"+str(len_point)
            str2 = str1 + "\n" + "Coordinates of points:" +str(points[0])
            label.setText(str2)

        if side == 'left':
            _show_point(parent,points,color='b',side='left')
        elif side == 'right':
            _show_point(parent,points,color='r',side='right')
    # parent.plotter.disable()
    parent.plotter.enable_point_picking(callback=_the_callback,
                                         left_clicking=True,
            show_message=show_message,
            use_mesh=True)

def _pick_left_line(parent,
            left_label = None):
    _pick_line(parent,color='b',side='left',
            label = left_label,)
  
def _show_point(parent, points,color='b',side = 'left'):
    bounds = parent.mesh.bounds
    interval = 100
    x = abs(bounds[1]-bounds[0])/interval
    y = abs(bounds[3]-bounds[2])/interval
    z = abs(bounds[5]-bounds[4])/interval
    # print(points.shape,len(points.shape))
    if len(points.shape) == 1:   
        mesh = pv.Cube(center=points, x_length=x, y_length=y, z_length=z)
        temp_actor = parent.plotter.add_mesh(mesh,style='surface',
                                             
                                            color=color,reset_camera=False)
        if side == 'left':
            parent.left_point_labels_actor.append(temp_actor)
        elif side == 'right':
            parent.right_point_labels_actor.append(temp_actor)
    else :
        for point in points:
            mesh = pv.Cube(center=point, x_length=x, y_length=y, z_length=z)
            temp_actor = parent.plotter.add_mesh(mesh,style='surface', 
                                                 pickable_window=False,
                                                 color=color,reset_camera=False)
            if side == 'left':
                parent.left_point_labels_actor.append(temp_actor)
            elif side == 'right':
                parent.right_point_labels_actor.append(temp_actor)

def _pick_left_point(parent,i,label=None):
    # parent.plotter.disable()
    def select_point_callback(point):

        length =  len(parent.left_point)
        if(i < length):
            str1 = label.text()
            str2 = "\nError, you can't select another point!\n"
            label.setText(str1+str2)
            # parent.label1.setText("Error, you can't select another point!")
            return 
        _show_point(parent,point,color='b',side='left')

        parent.left_point.append(point)
        # if label is  None:
        #     label = parent.label1
            # parent.label1.setText("Selected points:"+str(len(parent.left_point)))
        # else:
        label.setText("Selected points:"+str(len(parent.left_point)))
        str1 = label.text()
        str1 = str1 + "\n" + "Coordinates of points:" +str(parent.left_point)
        # parent.label1.setText(str1)
        label.setText(str1)
        # print("left")
        # print(parent.left_point,type(parent.left_point))
    # print("-----")
    # label.setText("------")
    # parent.plotter.disable()
    parent.plotter.enable_point_picking(callback=select_point_callback,
                                        left_clicking=True,
                                        pickable_window=False)

def _pick_right_line(parent,
            right_label = None):
    _pick_line(parent,color='r',side='right',        
            label = right_label)
   
def _pick_right_point(parent,i,label=None):
         
    # parent.plotter.disable()
    def select_point_callback(point):
        length =  len(parent.right_point)
        if(i < length):
            str1 = label.text()
            str2 = "\nError, you can't select another point!\n"
            label.setText(str1+str2)
            return 

        _show_point(parent,point,color='r',side='right')

        parent.right_point.append(point)
        label.setText("Selected points:"+str(len(parent.right_point)))
        str1 = label.text()
        str1 = str1 + "\n" + "Coordinates of points:" +str(parent.right_point)
        label.setText(str1)

    parent.plotter.enable_point_picking(callback=select_point_callback,
                                         left_clicking=True,
                                        pickable_window=False)

def _pick_left_face(parent,label=None):
    def select_face_callback(index):
        if index is None: return 
        for actor in parent.left_face_actor:
            parent.plotter.remove_actor(actor)
        parent.left_face_actor.clear()
        picked = index
        temp_actor = parent.plotter.add_mesh(
                    picked,
                    style='wireframe',
                    color='b',
                    line_width=5,
                    pickable=False,
                    reset_camera=False,)
        parent.left_face_actor.append(temp_actor)
        parent.left_point = [i for i in index.points]
        label.setText("The number of faces:"+str(len(parent.left_point)))
        str1 = label.text()
        str1 = str1 + "\n" + "Coordinates of points:" +str(parent.left_point)
        label.setText(str1)
    # parent.plotter.disable()
    parent.plotter.enable_cell_picking(callback=select_face_callback,
                        show=False,through=True,show_message=False)
    
def _pick_right_face(parent,label=None):

    def select_face_callback(index):
        for actor in parent.right_face_actor:
            parent.plotter.remove_actor(actor)
        parent.right_face_actor.clear()
        picked = index
        temp_actor = parent.plotter.add_mesh(
                    picked,
                    style='wireframe',
                    color='r',
                    line_width=5,
                    pickable=False,
                    reset_camera=False,)
        parent.right_face_actor.append(temp_actor)
        parent.right_point = [i for i in index.points]
        label.setText("The number of faces:"+str(len(parent.right_point)))
        str1 = label.text()
        str1 = str1 + "\n" + "Coordinates of points:" +str(parent.right_point)
        label.setText(str1)            
    # parent.plotter.disable()  
    parent.plotter.enable_cell_picking(callback=select_face_callback,
                    show_message=False,show = False, through=False)

def _distance_between_points(parent):
    # print()
    
    point1 = np.array(parent.left_point[0]) 
    point2 = np.array(parent.right_point[0])
    np_dis = point1 - point2
    distance = np.linalg.norm(np_dis)
    lines = np.array([point1,point2])
    # print(distance)
    # print("point1=",point1,lines)
    line_actor = parent.plotter.add_lines(lines, color='g',
                                          width=3,label=str(distance))
    # parent.plotter.add_legend()
    for actor in parent.line_actor:
        parent.plotter.remove_actor(actor)
    parent.line_actor.clear()

    parent.distLabel.setText("distance between points is :"+ str(distance))
    parent.line_actor.append(line_actor)

def _distance_between_point_and_line(parent):

    len_left_data = len(parent.left_point)
    len_right_data = len(parent.right_point)
    np_vector1 = np.array([])
    np_vector2 = np.array([])
    original_point=[]
    start_point = []
    
    if len_left_data== 1 and len_right_data == 2:
        np_vector1 = np.array(parent.right_point[1]) - np.array(parent.right_point[0]) 
        np_vector2 = np.array(parent.left_point) - np.array(parent.right_point[0])
        original_point = parent.left_point
        start_point = parent.right_point[0]

    if  len_left_data== 2 and len_right_data == 1:
        np_vector1 = np.array(parent.left_point[1]) - np.array(parent.left_point[0]) 
        np_vector2 = np.array(parent.right_point) - np.array(parent.left_point[0])
        original_point = parent.right_point
        start_point = parent.left_point[0]
    # print(np_vector1, np_vector2)

    unit_np_vector1 = np_vector1/np.linalg.norm(np_vector1)
    length = np.dot(unit_np_vector1,np_vector2[0])

    vertical_point = length*unit_np_vector1 + start_point
    dis_vect = vertical_point - original_point
    distance = np.linalg.norm(dis_vect)

    parent.distLabel.setText("distance between point and line is :"+ str(distance))
    # print()
    lines = np.array([vertical_point,original_point[0]])

    for actor in parent.line_actor:
        parent.plotter.remove_actor(actor)
    parent.line_actor.clear()

    line_actor = parent.plotter.add_lines(lines, color='g',width=6,label=str(distance))
    lines = np.array([vertical_point,start_point])
    line_actor1 = parent.plotter.add_lines(lines, color='y',width=1)
    parent.line_actor.append(line_actor)
    parent.line_actor.append(line_actor1)

def _distance_point_face_without_line(parent,normal_vector,point_in_plane,point_P):

    coeff_D = -np.dot(normal_vector,point_in_plane)
  
    dot_P_N = np.dot(normal_vector,point_P)
    # print("---- temp:",dot_P_N, dot_P_N + coeff_D)
    distance = (dot_P_N + coeff_D)/np.linalg.norm(normal_vector)
    # print("distance = " + str(distance))

    normal_vector= normal_vector/np.linalg.norm(normal_vector)
    vertical_point =  point_P - distance*normal_vector
    distance = abs(distance)
    return distance 

def _distance_point_face(parent,normal_vector,point_in_plane,point_P):

    coeff_D = -np.dot(normal_vector,point_in_plane)
  
    dot_P_N = np.dot(normal_vector,point_P)
    # print("---- temp:",dot_P_N, dot_P_N + coeff_D)
    distance = (dot_P_N + coeff_D)/np.linalg.norm(normal_vector)
    # print("distance = " + str(distance))

    normal_vector= normal_vector/np.linalg.norm(normal_vector)
    vertical_point =  point_P - distance*normal_vector
    distance = abs(distance)
    parent.distLabel.setText("Distance between point and face is :"
                             + str(distance))
    lines = np.array([vertical_point,point_P])

    for actor in parent.line_actor:
        parent.plotter.remove_actor(actor)
    parent.line_actor.clear()

    line_actor = parent.plotter.add_lines(lines, color='g',
                                          width=6,label=str(distance))
    # parent.line_actor.append(line_actor)

    lines = np.array([vertical_point,point_in_plane])
    line_actor1 = parent.plotter.add_lines(lines, color='y',width=1)
    parent.line_actor.append(line_actor)
    parent.line_actor.append(line_actor1)

def _distance_between_point_and_face(parent):
    """              A * x_0 + B * y_0 + C * z_0 + D
    # distance =  __________________________________
    #                        ||n||
    # where n(A,B,C) is normal vector of the plane  , point p(x_0, y_0, z_0) is outside the plane 
    """
    len_left_data = len(parent.left_point)
    len_right_data = len(parent.right_point)
    np_vector1 = np.array([])
    np_vector2 = np.array([])
    point_in_plane = np.array([])
    point_P = np.array([])

    if len_left_data== 1 and len_right_data == 3:
        np_vector1 = np.array(parent.right_point[1]) - np.array(parent.right_point[0]) 
        np_vector2 = np.array(parent.right_point[2]) - np.array(parent.right_point[0]) 
        point_in_plane = np.array(parent.right_point[0])
        point_P = np.array(parent.left_point[0])

    if len_left_data== 3 and len_right_data == 1:
        np_vector1 = np.array(parent.left_point[1]) - np.array(parent.left_point[0]) 
        np_vector2 = np.array(parent.left_point[2]) - np.array(parent.left_point[0]) 
        point_in_plane = np.array(parent.left_point[0])
        point_P = np.array(parent.right_point[0])

    normal_vector = np.cross(np_vector1,np_vector2)

    _distance_point_face(parent,normal_vector,point_in_plane,point_P)


def _distance_between_line_and_line(parent):
    np_vector1 = np.array(parent.right_point[1]) - np.array(parent.right_point[0]) 
    np_vector2 = np.array(parent.left_point[1]) - np.array(parent.left_point[0]) 

    cross_vect = np.cross(np_vector1,np_vector2)

    len_cross_vec = np.linalg.norm(cross_vect)
    # print("vec, len_vec", cross_vect, len_cross_vec)
    if abs(len_cross_vec)<1e-10:
        temp = parent.right_point[1]
        parent.right_point = []
        parent.right_point.append(temp)
        _distance_between_point_and_line(parent)
    else:
        parent.distLabel.setText("The two lines are not paralle, can't calculate distance!")

def _distance_between_line_and_face(parent):

    len_left_data = len(parent.left_point)
    len_right_data = len(parent.right_point)

    np_vector1 = np.array([])
    np_vector2 = np.array([])
    np_vector_line = np.array([])
    point_in_plane = np.array([])
    point_P = np.array([])

    if len_left_data== 2 and len_right_data == 3:
        np_vector1 = np.array(parent.right_point[1]) - np.array(parent.right_point[0]) 
        np_vector2 = np.array(parent.right_point[2]) - np.array(parent.right_point[0]) 
        np_vector_line = np.array(parent.left_point[1]) - np.array(parent.left_point[0])
        point_in_plane = np.array(parent.right_point[0])
        point_P = np.array(parent.left_point[0])

    if len_left_data== 3 and len_right_data == 2:
        np_vector1 = np.array(parent.left_point[1]) - np.array(parent.left_point[0]) 
        np_vector2 = np.array(parent.left_point[2]) - np.array(parent.left_point[0]) 
        np_vector_line = np.array(parent.right_point[1]) - np.array(parent.right_point[0])
        point_in_plane = np.array(parent.left_point[0])
        point_P = np.array(parent.right_point[0])

    normal_vector = np.cross(np_vector1,np_vector2)
    dot_value = np.dot(normal_vector,np_vector_line) # check if line is parallel to face 

    if abs(dot_value) < 1e-10:
        _distance_point_face(parent, normal_vector,point_in_plane,point_P)
    else :
        parent.distLabel.setText("Line is not parallel to the face, can't calculate the distance in this case")

def _distance_between_face_and_face(parent,show_line=True):
    left_vector1 = np.array(parent.left_point[1]) - np.array(parent.left_point[0]) 
    left_vector2 = np.array(parent.left_point[2]) - np.array(parent.left_point[0]) 

    right_vector1 = np.array(parent.right_point[1]) - np.array(parent.right_point[0]) 
    right_vector2 = np.array(parent.right_point[2]) - np.array(parent.right_point[0]) 

    left_normal_vector = np.cross(left_vector1,left_vector2)
    right_normal_vector = np.cross(right_vector1,right_vector2)

    # if dot product of two vectors is zero vector, there are parallel
    test_vector = np.cross(left_normal_vector,right_normal_vector)
    vector_value = np.linalg.norm(test_vector)
    # print("testwst",vector_value)
    if abs(vector_value) < 1e-6:
        
        point_in_plane = np.array(parent.left_point[0])
        point_P = np.array(parent.right_point[0])
        if show_line:
            _distance_point_face(parent,left_normal_vector,point_in_plane,point_P)
        else :
            distance = _distance_point_face_without_line(
                parent,left_normal_vector,point_in_plane,point_P)
            # print("dist = ",distance )
            return distance

            
    else :
        if show_line:
            parent.distLabel.setText("The two faces are not parallel,  \\\
            can't calculate distance in this case")
        # else :
        #     print("The two faces are not parallel, can't calculate distance in this case")