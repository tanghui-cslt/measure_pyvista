import pyvista as pv
from pyvista import examples,_vtk
# from pyvista.utilities.arrays import _coerce_pointslike_arg
import numpy as np
import sys,os 
# mesh =examples.load_nut()
# mesh = pv.read('F://twoCylinder1.ply')
import copy,math 
class Find_CirCle:

    def __init__(self,plotter,mesh):
        self.mesh = mesh
        
        self.mesh= self.mesh.compute_normals()
        self.p = plotter
        self.p.add_mesh(self.mesh,style='wireframe')
    
    def _init_edge_dict_from_mesh(self):
        # mesh = self.mesh 
        new_dict = {}
        for cells in self.mesh.cell:
            for edge in  cells.edges:
                pids = edge.point_ids
                pids.sort()
                edge_id = str(pids[0])+"+"+str(pids[1])
                new_dict[edge_id] = False
        return new_dict


    def _seperate_connected_components(self,
                    finished_list,searching_list,edge_list):

        if(len(edge_list) == 0 and len(searching_list) == 0 ):
            return 
        if len(searching_list)>0:
            set_start_list = set([])
            for edge in searching_list:
                start_id = set(edge.point_ids)
                set_start_list = set_start_list | start_id
            # start_edge = start_edge_list[0]
        else:
            start_edge = edge_list[0]
            # searching_list.append(start_edge)
            set_start_list = set(start_edge.point_ids)

        temp_list = []
        flag_find_result = False
        for edge in edge_list:
            temp_line_id = edge.point_ids
            set_temp_line_id = set (temp_line_id)
            new_id =  set_start_list & set_temp_line_id
            if len(new_id) > 0:

                set_start_list = set_start_list | set_temp_line_id
                flag_find_result = True
                searching_list.append(edge)
                temp_list.append(edge)

        for edge in temp_list:
            edge_list.remove(edge)

        if flag_find_result==False:
            finished_list.append(searching_list)
            # print("test",len(finished_list[0]))
            searching_list = []
        self._seperate_connected_components(finished_list,
                                    searching_list,edge_list)


    def _calc_radius_from_three_points(self,points):
        A = np.array(points[0])
        B = np.array(points[1])
        C = np.array(points[2])
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

        polar = center-points[2] 

        return center,polar,R

    def _is_a_point_on_circle(self,center,R,point):
        num = 0
        R1 = np.linalg.norm(np.array(point-center))
        # print("abs = ",abs(R1-R) )
        if abs(R1-R)<0.001:
            num = 1
        return num

    def _calc_cylinder_boundary(self):
        """
        The key to find a cylinder by determing the sides of a polygon that the 
        two faces adjacent to it are perpendicular
        In other cases, such as an open cylinder, one just need additionally 
        process the boundary edges of the mesh which may be also a circle 
        
        """
        mesh = self.mesh
        edge_dict = self._init_edge_dict_from_mesh()
        # num = 0
        edge_list = []
        for cells in mesh.cell:
            for i in  range(3):
                edge =cells.get_edge(i)
                pids = edge.point_ids
                pids.sort()
                edge_id = str(pids[0])+"+"+str(pids[1])
                value = edge_dict[edge_id]
                if value == True:
                        continue

                # num = num + 1
                edge_dict[edge_id] = True
                points = edge.points
                index = mesh.find_cells_along_line(points[0],points[1])

                cell_id_list = []
                cell_list = []
                # print("----:",edge.point_ids.sort())
                for i in index:
                    single_cell = mesh.get_cell(i)
                    cell_point_ids = single_cell.point_ids
                    # print("-----",cell_point_ids)
                    # flag = _is_edge_in_cell(edge,single_cell)
                    if set(pids) < set(cell_point_ids):
                        cell_list.append(single_cell)
                        cell_id_list.append(i)
                    
                new_index = cell_id_list
                # print("new_index---",new_index)
                normals = mesh.cell_data['Normals'][new_index,:]
                normal = normals[0]
                dot_value = np.dot(normals,normal.transpose())

                # mesh.cell[index,:]
                tempa = dot_value>-0.1
                tempb = dot_value<0.1
                tempc = dot_value>0.9
                tempd = dot_value<1.1
                temp_min = tempa&tempb
                temp_max = tempc&tempd
                num_min = np.sum(temp_min)
                num_max = np.sum(temp_max)
                if (num_min + num_max == len(dot_value) 
                    and (num_min >0 and num_max>0)):
                    edge_list.append(edge)
        # print("num = ",num)
        return edge_list

    def _get_cylinder_boundary(self):
        """
        seperate different components from cylinder boundary
        """
        edge_list = self._calc_cylinder_boundary()
        # self._generate_indices_dict(edge_list)

        finished_list = []
        searching_list = []
        self._seperate_connected_components(
            finished_list,searching_list,edge_list)
        return finished_list


    def _calc_circle_from_edge_list(self,
                edge_list, edge_id_list,circle_list,total_num = 4):
        """
        get different circles from diferent connected components
        """    
        len_edge = len(edge_list)
        start_edge_id = edge_id_list[0]
        end_edge_id = edge_id_list[1]
        if (edge_id_list[1] > len_edge-1):
            edge_id_list[0] += 1
            edge_id_list[1] = edge_id_list[0] + 1
            # print("edet_id ------",edge_id_list)
            # if(start_edge_id == len_edge-1):
                # return 
        if(edge_id_list[0] > len_edge-2):

            return 
            
        # print("edet_id ",edge_id_list)
        if edge_id_list[0] == edge_id_list[1]:
            edge_id_list[1] = edge_id_list[0] + 1

        start_edge_id = edge_id_list[0]
        end_edge_id = edge_id_list[1]
        start_points = np.array(edge_list[start_edge_id].points)
        three_points  =  np.vstack((start_points[0],start_points[1]))

        end_points =  edge_list[end_edge_id].points
        # test_flag = False
        angle =  0
        for point in end_points:
            temp0 = three_points[0]
            temp1 = three_points[1]

            if ((point==temp0).all() ==False
                ) and ((point==temp1).all() ==False)  :
                three_points   = np.vstack(
                    (start_points[0],start_points[1],point))
                np_vec1 =  start_points[1]-start_points[0]
                np_vec2 = point-start_points[0]
                normal_verctor = np.cross(np_vec1,np_vec2)
                normal_verctor = normal_verctor/np.linalg.norm(normal_verctor)
                dot_value = np.dot(np_vec1,np_vec2)
                norm1 = np.linalg.norm(np_vec1)
                norm2 = np.linalg.norm(np_vec2)
                cos1_2 = dot_value/(norm1*norm2)
                angle = np.arccos(cos1_2)/math.pi*180               
                break
                   
        
        #determin whether three points are in a line 
        if abs(abs(angle ) - 1) < 1e-3:
            # print(three_points)
            edge_id_list[1] += 1

            self._calc_circle_from_edge_list(
                edge_list, edge_id_list,circle_list,total_num )
            # print("three points are in a line" )
            return  
  
        if(len(three_points)== 2):

            edge_id_list[1] += 1
            self._calc_circle_from_edge_list(
                edge_list, edge_id_list,circle_list,total_num )
            return 
        center,polar,R = self._calc_radius_from_three_points(three_points)
        num = 0
        for edge in edge_list:
            start_points = edge.points
            num += self._is_a_point_on_circle(center,R,start_points[0])
            num += self._is_a_point_on_circle(center,R,start_points[1])
        num = num /2
        print("num, length",num , len_edge,edge_id_list)
        if  (num > len_edge/2 or   num > len_edge-5 ) and num >=total_num:
        # if  (num > len_edge/2 or   num > len_edge-5) and num >11:
            circle_list[0] = center
            circle_list[1] = polar
            circle_list[2] = R
            circle_list[3] = normal_verctor
            print("the num of points on cirlcle",num)
            return 
        
        else:
            edge_id_list[1] += 1
            self._calc_circle_from_edge_list(
                edge_list, edge_id_list,circle_list,total_num )


    def _find_circles_from_components(self,
                    finished_list,edge_id_list= [0,0],total_num = 4):
        """
        get circles on same cylinder.
        finished_list 是不同的连通分支,
        edge_id_list 是计算圆需要的三个点的边的起始id, 递归来穷举所有的边.
        total_num 最小的数量形成一个圆, 找圆的是4, cylinder是10

        """
        edge_id_list = [0,0]
        circle_list = []
        # single_circle_list = [0,1,2,3]
        for edge_list in finished_list:
            edge_id_list = [0,0]
            single_circle_list = [0,1,2,3]
            print("the number of the componet", len(edge_list))
            self._calc_circle_from_edge_list(
                edge_list,edge_id_list,single_circle_list,total_num)
            list_flag = isinstance(single_circle_list[0],np.ndarray)
            #if the component is not a circle, continue 
            if(list_flag==False):
                continue
            # print("single_circle_list",single_circle_list)
            circle_list.append(single_circle_list)
            
        return circle_list

    def _is_paralleled(self,origin_normal_verctor,normal_verctor1,new_center):
        new_center = new_center/np.linalg.norm(new_center)
        dot_value_1 = np.dot(origin_normal_verctor,normal_verctor1)
        dot_value_2 = np.dot(origin_normal_verctor,new_center)
        dot_value_3 = np.dot(new_center,normal_verctor1)
        # print("value = ",dot_value_1,dot_value_2,dot_value_3)
        dot_value_1 = abs(abs(dot_value_1)-1)
        dot_value_2 = abs(abs(dot_value_2)-1)
        dot_value_3 = abs(abs(dot_value_3)-1)
        if dot_value_1<1e-2 and dot_value_2<1e-2 and dot_value_3<1e-2 :
            return True
        return False 
    
    def _find_elementId_from_list(self,single_list,list_data):
        #查找多维list的元素的id,如果直接用in 某个list是否在另一个
        # list里面,会出问题
        len_single_data = len(single_list)
        # print("s= ", single_list)
        # print("ls= ", list_data)
        for i,data in zip(range(len(list_data)), list_data):
            # print("data=",i,data)
            # list_flag = isinstance(data,list)
            
            len_data = len(data)
            if len_single_data == len_data:
                num = 0
                for j in range(len_data):
                    list_flag = isinstance(data[j],np.ndarray)
                    if list_flag:
                        # print (single_list[j])
                        if (single_list[j] == data[j] ).all():
                            num += 1 
                    else:
                        if (single_list[j] == data[j] ):
                            num += 1 
                if num ==  len_data:
                    return i
                # else :
                    # print("num = ", num ,)
                    # return -1
            else:
                return -1

    def _get_boundary_edges(self):
        boundary_edges = self.mesh.extract_feature_edges(
        boundary_edges=True, feature_edges=False, manifold_edges=False)
        edge_list = []
        for i in range(boundary_edges.n_cells):
            edge = boundary_edges.get_cell(i)
            edge_list.append(edge)
            # print(edge)
        finished_list = []
        searching_list = []
        self._seperate_connected_components(
            finished_list,searching_list,edge_list)
        # self._show_circle_edge(finished_list)
        return finished_list

    def _show_components(self,finished_list):
        num = 0
        for start_edge_list in finished_list:
            print("num = ",num,len(start_edge_list))
            # print("len = ", len(start_edge_list))
            # num_edge=0
            for edge in start_edge_list:
                points = edge.points
                self.p.add_lines(points,color='r')
            num = num +1

    def _show_circle_edge(self,circle_list):
        num = 0
        color = ['r','g','b','y']

        print("len = ",len(circle_list))
        for single_circle in circle_list:
            # center_list.append(single_circle[0])
            arc = pv.CircularArcFromNormal(single_circle[0],
            resolution=100,polar=single_circle[1],
            normal=single_circle[3], angle=360)
            circle_actor = self.p.add_mesh(arc,
            color=color[num], line_width=4, 
            reset_camera=False,show_edges = True)
            num = num +1

    def find_circle(self):
        cylinder_list = self._get_cylinder_boundary()
        #get boundary_edges 
        boundary_list = self._get_boundary_edges()
        # self.p.show()
        edge_id_list = [0,0]
        # print("bl",boundary_list)
        finished_list = cylinder_list + boundary_list

        self._show_components(finished_list)
        # self.p.show()
        # get [center,polar, R, normal_verctor ]
        circle_list = self._find_circles_from_components(
            finished_list,edge_id_list,total_num = 4)
        # self._show_circle_edge(circle_list)
        self.p.show()




class Find_Cylinder(Find_CirCle):

    def __init__(self,plotter,mesh):
        # FindCirCle.__init__(self,plotter,mesh)
        super().__init__(plotter,mesh)
    
    def _sperata_circle_from_components(
            self,finished_list,searching_list,circle_list):
        """
        determine which circles are on the same cylinder.
        结果存在finished_list中,每一个子list都是一个cirlce或者cylinder
        如果是单个圆的话,他的list中只有一个子list
        如果是cylinder的话,他的list中有两个子list
        """
        if(len(circle_list) == 0 and len(searching_list) == 0 ):
            return 
        if len(searching_list)>0:
            single_circle = searching_list[0]

        else:
            single_circle = circle_list[0]
        temp_list = []
        flag_find_result = False

        origin_center = single_circle[0]
        origin_R = single_circle[2]
        origin_normal_verctor = single_circle[3]

        for circle in circle_list:

            center1 = circle[0]
            R1 = circle[2]
            normal_verctor1 = circle[3]
            new_center = center1 - origin_center
            if np.linalg.norm(new_center)<1e-10:
                new_center = normal_verctor1
            if abs(origin_R - R1)<0.05:
                flag = self._is_paralleled(
                    origin_normal_verctor,normal_verctor1,new_center)
                
                if flag :
                    flag_find_result = True
                    searching_list.append(circle)
                    temp_list.append(circle)

        for circle in temp_list:
            id = self._find_elementId_from_list(circle,circle_list)
            # print("id = ",id )
            del circle_list[id]

        if flag_find_result==False:
            finished_list.append(searching_list)
            searching_list = []
        self._sperata_circle_from_components(
            finished_list,searching_list,circle_list)

    def _find_cylinder_from_circles(self,circle_list):
        cylinder_list = []
        searching_list = []
        
        self._sperata_circle_from_components(
            cylinder_list,searching_list,circle_list)
        return cylinder_list
        
    def _show_cylinder(self,cylinder_list):
        color = ['r','g','b','y']
        num = 0
        for circle in cylinder_list:
            # origin_circle = circle[0]
            j = 0
            center_list = []
            for single_circle in circle:
                center_list.append(single_circle[0])
                arc = pv.CircularArcFromNormal(single_circle[0],
                resolution=100,polar=single_circle[1],
                normal=single_circle[3], angle=360)
                circle_actor = self.p.add_mesh(arc,
                color=color[num], line_width=4, 
                reset_camera=False,show_edges = True)
                if (j==1):
                    self.p.add_lines(np.array(center_list),color=color[num])
                # print("R = ",single_circle[2])
                j += 1
            num += 1
        self.p.show()

    def find_cylinder(self):
        # mesh = self.mesh
        cylinder_list = self._get_cylinder_boundary()
        #get boundary_edges 
        boundary_list = self._get_boundary_edges()
        # self.p.show()
        edge_id_list = [0,0]
        # print("bl",boundary_list)
        finished_list = cylinder_list + boundary_list
        # get [center,polar, R, normal_verctor ]
        circle_list = self._find_circles_from_components(
            finished_list,edge_id_list,total_num=9)
        # self._show_circle_edge(circle_list)
        print("len = ",len(circle_list))
        # find two circles on the same cylinder
        cylinder_list = self._find_cylinder_from_circles(circle_list)
        return cylinder_list
        # self._show_cylinder(cylinder_list)
        # self.p.show()

def result():
    mesh =pv.Cylinder(center=[1, 2, 3], direction=[1, 1, 1],
                                radius=1, height=2).triangulate()
    # mesh = examples.load_Cylinder()
    # mesh = pv.read('F:/twoCylinder1.ply')
    # mesh = pv.read('F:/Cut_Box.stl')
    # # mesh = pv.read('F://twoCylinder3.ply')
    plotter = pv.Plotter()
    fv = Find_Cylinder(plotter,mesh)
    cylinder_list = fv.find_cylinder()
    # fv._show_cylinder(cylinder_list)
    # plotter.show()
    # fcircle = Find_CirCle(plotter,mesh)
    # fcircle.find_circle()

# fcircle = Find_CirCle(plotter,mesh)
    # fcircle.find_circle()
# mesh = pv.read('F://Cut_Box.ply')
# mesh = pv.read('F:/twoCylinder1.ply')
# mesh = examples.load_Cylinder()
# # mesh = pv.read('F://twoCylinder3.ply')
#     # mesh = examples.load_Cylinder()
# plotter = pv.Plotter()

# fv = Find_Cylinder(plotter,mesh)
# cylinder_list = fv.find_cylinder()
# fv._show_cylinder(cylinder_list)

# fcircle = Find_CirCle(plotter,mesh)
# fcircle.find_circle()

# def load_Cylinder():

#     """
#     return pyvista.read(os.path.join(dir_path, 'Cylinder1.ply'))