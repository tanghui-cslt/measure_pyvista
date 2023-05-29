import pyvista  as pv
import numpy as np
from pyvista import _vtk
from pyvista.utilities import try_callback
import math 
def _angle_between_line_and_line(parent,label):
    np_vector1 = np.array(parent.right_point[1]) - np.array(parent.right_point[0]) 
    np_vector2 = np.array(parent.left_point[1]) - np.array(parent.left_point[0]) 
    dot_value = np.dot(np_vector1,np_vector2)
    norm1 = np.linalg.norm(np_vector1)
    norm2 = np.linalg.norm(np_vector2)
    cos1_2 = dot_value/(norm1*norm2)
    angle = np.arccos(cos1_2)/math.pi*180
    the_other_angle = 180 - angle 
    label.setText("angle is "+str(angle)+ ", \n or is "+str(the_other_angle))
    # print()

def  _angle_between_line_and_face(parent,label):
    len_left_data = len(parent.left_point)
    len_right_data = len(parent.right_point)

    np_vector1 = np.array([])
    np_vector2 = np.array([])
    np_vector_line = np.array([])

    if len_left_data== 2 and len_right_data == 3:
        np_vector1 = np.array(parent.right_point[1]) - np.array(parent.right_point[0]) 
        np_vector2 = np.array(parent.right_point[2]) - np.array(parent.right_point[0]) 
        np_vector_line = np.array(parent.left_point[1]) - np.array(parent.left_point[0])
    

    if len_left_data== 3 and len_right_data == 2:
        np_vector1 = np.array(parent.left_point[1]) - np.array(parent.left_point[0]) 
        np_vector2 = np.array(parent.left_point[2]) - np.array(parent.left_point[0]) 
        np_vector_line = np.array(parent.right_point[1]) - np.array(parent.right_point[0])
    normal_vector = np.cross(np_vector1,np_vector2)

    dot_value = np.dot(normal_vector,np_vector_line)

    norm1 = np.linalg.norm(normal_vector)
    norm2 = np.linalg.norm(np_vector_line)
    cos1_2 = dot_value/(norm1*norm2)
    # print("cos12",np.arccos(cos1_2))
    temp_angle = np.arccos(cos1_2)/math.pi*180
    the_other_angle = 180 - temp_angle 

    angle = 0
    # print( "-----",temp_angle,the_other_angle)
    if temp_angle<= 90:
        angle = 90 - temp_angle
    else:
        angle = 90 - the_other_angle
    label.setText("angle is :"+str(angle))


def _angle_between_face_and_face(parent,label):
    left_vector1 = np.array(parent.left_point[1]) - np.array(parent.left_point[0]) 
    left_vector2 = np.array(parent.left_point[2]) - np.array(parent.left_point[0]) 

    right_vector1 = np.array(parent.right_point[1]) - np.array(parent.right_point[0]) 
    right_vector2 = np.array(parent.right_point[2]) - np.array(parent.right_point[0]) 

    left_normal_vector = np.cross(left_vector1,left_vector2)
    right_normal_vector = np.cross(right_vector1,right_vector2)

    dot_value = np.dot(left_normal_vector,right_normal_vector)

    norm1 = np.linalg.norm(left_normal_vector)
    norm2 = np.linalg.norm(right_normal_vector)
    cos1_2 = dot_value/(norm1*norm2)
    # print("cos12",np.arccos(cos1_2))
    angle = np.arccos(cos1_2)/math.pi*180
    the_other_angle = 180 - angle 
    label.setText("angle is "+str(angle)+ ", \n or is "+str(the_other_angle))