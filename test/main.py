import sys,os
os.environ["QT_API"] = "pyqt5"
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QTextEdit,QFormLayout,QSplashScreen,QFrame 
import pyvista as pv
from pyvista import examples
from pyvistaqt import BackgroundPlotter, QtInteractor, MainWindow
from Ui_main import Ui_MainWindow #导入QtTest文件
import numpy as np


class MyMainWindows(MainWindow,Ui_MainWindow):
    def __init__(self):

        super(MyMainWindows, self).__init__()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_widgt = QtWidgets.QWidget()
        self.main_widgt.setLayout(self.main_layout)
        self.left_widget = QtWidgets.QWidget()
        self.right_widget = QtWidgets.QWidget()
        self.init_ui()

    def init_ui(self):
        self.init_left()
        self.init_right()

        self.main_layout.addWidget(self.left_widget)
        self.main_layout.addWidget(self.right_widget)
        self.main_layout.setStretchFactor(self.left_widget,3)
        self.main_layout.setStretchFactor(self.right_widget,1)
        self.setCentralWidget(self.main_widgt)
        # self.resize(950,650)
        self.setWindowFilePath("Test")
        self.show()

    def init_left(self):

        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()
        self.plotter = QtInteractor(self.left_widget)
        vlayout.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)
        self.left_widget.setLayout(vlayout)
        
    def init_right(self):
        vlayout = QtWidgets.QVBoxLayout()
        self.btn1 = QtWidgets.QPushButton("Show object")
        self.toolBox = QtWidgets.QToolBox()
        self.setupTool1()
        self.setupTool2()

        self.toolBox.setCurrentIndex(0)
        vlayout.addWidget(self.btn1)
        vlayout.addWidget(self.toolBox)
        self.right_widget.setLayout(vlayout)
        self.btn1.clicked.connect(self.add_mesh)
        self.bound_flag = False

    def setupTool1(self):
        frame=QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.WinPanel|QtWidgets.QFrame.Raised)
        layout = QtWidgets.QGridLayout()
        self.label1 =  QtWidgets.QLabel("Left side")
        self.clearBtn1 = QtWidgets.QPushButton('Clear points')
        self.clearBtn1.clicked.connect(self.clear_left_data)

        self.comboBox1 = QtWidgets.QComboBox()
        self.comboBox1.addItem("point")
        self.comboBox1.addItem("line")
        self.comboBox1.addItem("face")
        self.comboBox1.activated.connect(self.selectionChanged1)
        

        self.label2 =  QtWidgets.QLabel("Right side")
        self.clearBtn2 = QtWidgets.QPushButton('Clear points')
        self.clearBtn2.clicked.connect(self.clear_right_data)
        self.comboBox2 = QtWidgets.QComboBox()
        self.comboBox2.addItem("point")
        self.comboBox2.addItem("line")
        self.comboBox2.addItem("face")
        self.comboBox2.activated.connect(self.selectionChanged2)

        self.calcDistBtn = QtWidgets.QPushButton('Calc distance')
        self.calcDistBtn.clicked.connect(self.calc_distance)

        self.distLabel = QtWidgets.QLabel()
        self.distLabel.setStyleSheet("background-color: white")
        self.distLabel.setAutoFillBackground(True)
        
        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.clearBtn1,0,1)
        layout.addWidget(self.comboBox1,1,0,1,2)

        layout.addWidget(self.label2, 3, 0)
        layout.addWidget(self.clearBtn2,3,1)
        layout.addWidget(self.comboBox2,4,0,1,2)
        layout.addWidget(self.calcDistBtn,5,0,1,2)
        layout.addWidget(self.distLabel,6,0,2,2)
    

        frame.setLayout(layout)
        self.toolBox.addItem(frame, "Distance ")

    def setupTool2(self):

        frame=QtWidgets.QFrame()
        layout = QtWidgets.QVBoxLayout()
        self.button1 = QtWidgets.QPushButton("Radius of Circle")
        self.button2 = QtWidgets.QPushButton("Radius of Cyclinder")
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        frame.setLayout(layout)
        self.toolBox.addItem(frame, "Radius ")

    def add_mesh(self):
        self.plotter.clear()
        self.mesh =  examples.download_bunny_coarse().triangulate()
        self.plotter.add_mesh(self.mesh,style='wireframe', show_edges=True,pickable=True)

        # bounds 
        if self.bound_flag:
            self.plotter.show_bounds(
                grid='front',
                location='outer',
                all_edges=True,
            )
            
        # self.plotter.reset_camera()
        self.bound_flag = ~ self.bound_flag 

    def pick_left_point(self):
        self.left_point=[]
        self.left_point_labels_actor=[]

        def select_point_callback(point):

            mesh = pv.Cube(center=point, x_length=0.005, y_length=0.005, z_length=0.005)
            temp_actor = self.plotter.add_mesh(mesh, style='wireframe', color='b')
            # temp_actor = self.plotter.add_point_labels(point, 
                        #                   [
                        # f"{point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f}"
                        #                 ], point_color='blue')
            self.left_point_labels_actor.append(temp_actor)
            self.left_point.append(point)
            print("left")
            print(self.left_point)

        self.plotter.enable_point_picking(callback=select_point_callback,pickable_window=False)

    def pick_right_point(self):
        self.right_point=[]
        self.right_point_labels_actor=[]
        def select_point_callback(point):
            mesh = pv.Cube(center=point, x_length=0.005, y_length=0.005, z_length=0.005)
            temp_actor = self.plotter.add_mesh(mesh, style='wireframe', color='r')
            # temp_actor = self.plotter.add_point_labels(point, 
            #                               [
            #             f"{point[0]:.2f}, {point[1]:.2f}, {point[2]:.2f}"
            #                             ], point_color = 'red')
            self.right_point.append(point)
            self.right_point_labels_actor.append(temp_actor)
            print("right")
            print(self.right_point)

        self.plotter.enable_point_picking(callback=select_point_callback,pickable_window=False)

    def pick_line(self):

        def select_line_callback(points):
            print(points)
            
        self.plotter.enable_cell_picking(callback=select_line_callback,through=False,left_clicking=True,color='r')
        self.plotter.add_points(self.sphere.points, pickable=False, color='red', render_points_as_spheres=True)

    def selectionChanged1(self,i):
        
        self.number_points=0
        self.pick_left_point()
        self.distLabel.setText('selecting left point')
        
    def selectionChanged2(self,i):
        
        self.number_points=0
        self.pick_right_point()
        self.distLabel.setText('selecting right point')

    def clear_left_data(self):
        if len(self.left_point_labels_actor) == 0 | len(self.left_point) == 0:
            return 
        for temp_actor in self.left_point_labels_actor:
            self.plotter.remove_actor(temp_actor)

        self.left_point.clear()
  
    def clear_right_data(self):
        
        if len(self.right_point_labels_actor) == 0 | len(self.right_point) == 0:
            return 
        for temp_actor in self.right_point_labels_actor:
            self.plotter.remove_actor(temp_actor)
        self.right_point.clear()

    def calc_distance(self):
        len_left_data = len(self.left_point)
        len_right_data = len(self.right_point)
        if len_left_data == 1 & len_left_data == 1:
            self.distance_between_point()

    def distance_between_point(self):
        np_dis = np.array(self.left_point) - np.array(self.right_point)
        dist = np.linalg.norm(np_dis)
        self.distLabel.setText("distance between points is :"+ str(dist))

        # self.distLabel.setText(str(dist))


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    window =  MyMainWindows()
    sys.exit(app.exec_())
    # #获取UIC窗口操作权限
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # #调自定义的界面（即刚转换的.py对象）
    # Ui = Ui_main.Ui_MainWindow() 
    # Ui.setupUi(MainWindow)
    # #显示窗口并释放资源
    # MainWindow.show()
    # sys.exit(app.exec_())