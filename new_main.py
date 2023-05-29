import sys,os
os.environ["QT_API"] = "pyqt5"
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QTextEdit,QFormLayout,QSplashScreen,QFrame 
import pyvista as pv
from pyvista import examples
from pyvistaqt import BackgroundPlotter, QtInteractor, MainWindow
from Ui_main import Ui_MainWindow #导入QtTest文件
import numpy as np
import vtk

import distance
import radius
import show_object
import angle

class MyMainWindows(MainWindow,Ui_MainWindow):
    def __init__(self):

        super(MyMainWindows,self).__init__()
        self.setupUi(self)
        vlayout = QtWidgets.QVBoxLayout()
        self.plotter = QtInteractor(self.leftFrame)
        vlayout.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)
        self.leftFrame.setLayout(vlayout)
        self.showBoundsBtn.clicked.connect(self.show_bounds)

        self.bound_flag = False
        self.flag_wire_surface = True
        self.mesh = None
        self.vtkPolyData =None

        self.clearAllActorsBtn.clicked.connect(
           self.clear_all)
        
        self.clearBtn1.clicked.connect(
            lambda:self.clear_left_data(self.label1))
        self.clearBtn2.clicked.connect(
            lambda:self.clear_right_data(self.label2))
        slotcomboBox1 = lambda i: self.select_left_side(
            i,offset=0,label=self.distLabel,
            left_label =self.label1)
        self.comboBox1.activated.connect(slotcomboBox1)

        slotcomboBox2 = lambda i: self.select_right_side(
            i,offset=0,label=self.distLabel,
            right_label =self.label2)
        self.comboBox2.activated.connect(slotcomboBox2)

        self.calcDistBtn.clicked.connect(self.calc_distance)
        self.showObject.activated.connect(self.select_object)

        slotcomboBox = lambda i: self.select_left_side(
            i,offset=1,label=self.radiusLabel,
            left_label =self.label,)
        self.comboBox.activated.connect(slotcomboBox)

        slotcomboBox_2 = lambda i: self.select_right_side(
            i,offset=1,label=self.radiusLabel,
            right_label =self.label_2)
        self.comboBox_2.activated.connect(slotcomboBox_2)

        self.clearRadiusBtn1.clicked.connect(
            lambda:self.clear_left_data(self.label))
        self.clearRadiusBtn2.clicked.connect(
            lambda:self.clear_right_data(self.label_2))
        self.selectCircleBtn.clicked.connect(self.select_circle)
        self.wireSurfaceBtn.clicked.connect(self.wire_surface)

        self.calcAngleBtn.clicked.connect(
            lambda:self.calc_angle(self.radiusLabel))

        self.selectCylinderBtn.clicked.connect(self.select_cylinder)
        #set label to auto scroll 
        self.scrollBar = self.scrollArea.verticalScrollBar()
        slot_scrollBar = lambda : self.handleScrollBarRangeChanged(
            self.scrollBar)
        self.scrollBar.rangeChanged.connect(slot_scrollBar)

        self.scrollBar_2 = self.scrollArea_2.verticalScrollBar()
        slot_scrollBar_2 = lambda : self.handleScrollBarRangeChanged(
            self.scrollBar_2)
        self.scrollBar_2.rangeChanged.connect(slot_scrollBar_2)

        self.scrollBar_3 = self.scrollArea_3.verticalScrollBar()
        slot_scrollBar_3 = lambda : self.handleScrollBarRangeChanged(
            self.scrollBar_3)
        self.scrollBar_3.rangeChanged.connect(slot_scrollBar_3)

        self.scrollBar_4 = self.scrollArea_4.verticalScrollBar()
        slot_scrollBar_4 = lambda : self.handleScrollBarRangeChanged(
            self.scrollBar_4)
        self.scrollBar_4.rangeChanged.connect(slot_scrollBar_4)

        self.surfaceAreaBtn.clicked.connect(
            lambda:self.calc_area(self.label_4))
        self.volumeBtn.clicked.connect(
            lambda:self.calc_volume(self.label_5))

        self.left_point=[]
        self.left_point_labels_actor=[]
        self.right_point=[]
        self.right_point_labels_actor=[]
        self.line_actor = []
        self.left_line_actor=[]
        self.right_line_actor=[]
        self.face_actor=[]
        self.left_line_points = []
        self.right_line_points = []
        self.left_face_actor=[]
        self.right_face_actor=[]
        
        self.radius_actor= []
        
    def show_bounds(self):
        show_object._show_bounds(self)

    def handleScrollBarRangeChanged(self,scrollbar):
        maxValue = scrollbar.maximum()
        scrollbar.setValue(maxValue)
        # self.scrollButtonFlag = False

    def wire_surface(self):
        actor_list = []
        
        actor_list.append(self.left_point_labels_actor)
        actor_list.append(self.right_point_labels_actor)
        actor_list.append(self.line_actor)
        show_object._wire_surface(self,actor_list)
 

    def pick_left_point(self,i,left_label = None):
        distance._pick_left_point(self,i,label = left_label)

    def pick_right_point(self,i,right_label = None):
        distance._pick_right_point(self,i,label = right_label)

    def pick_left_line(self,
            left_label = None):
        distance._pick_left_line(self,
            left_label = left_label)

    def pick_right_line(self,
            right_label = None):
        distance._pick_right_line(self,
            right_label = right_label)

    def pick_left_face(self,label):
        distance._pick_left_face(self,label=label)


    def pick_right_face(self,label):
        distance._pick_right_face(self,label=label)

    def select_circle(self):
        picker = radius.Picker_circle(self.plotter, self.mesh,
                                       self.circleLabel,self.radius_actor)
        self.plotter.track_click_position(picker, side='right')

    def select_left_side(self,i,offset=0,label=None,
            left_label = None,):
        
        i = i + offset 
        # print("name= ",left_label.objectName())
        if i == 0 :
            self.pick_left_point(i,left_label = left_label)
        elif i ==1:
            self.pick_left_line(
            left_label = left_label,)
        else:
            self.pick_left_face(label=left_label)
        label.setText('Selecting left side')
        
    def select_right_side(self,i,offset=0,label=None,
            right_label = None):
        i = i + offset      
        if i == 0 :
            self.pick_right_point(i,right_label = right_label)
        elif i == 1:
            self.pick_right_line(right_label = right_label)
        else :
            self.pick_right_face(label=right_label)
        label.setText('Selecting right side')

    def select_object(self,i):
        show_object._select_object(self,i)

    def clear_left_data(self,lable):
        if len(self.left_point_labels_actor) != 0 :
            for temp_actor in self.left_point_labels_actor:
                self.plotter.remove_actor(temp_actor)
            self.left_point_labels_actor.clear()

        if len(self.left_line_actor) != 0 :
            for temp_actor in self.left_line_actor:
                self.plotter.remove_actor(temp_actor)
            self.left_line_actor.clear()

        if len(self.left_point) != 0:
            self.left_point.clear() 

        self.left_line_points.clear()
        if len(self.left_face_actor) != 0:
            for actor in self.left_face_actor:
                self.plotter.remove_actor(actor)
            self.left_face_actor.clear()

        lable.setText("Selected points:"+str(len(self.left_point)))
  
    def clear_right_data(self,label):
        if len(self.right_face_actor) != 0:
            for actor in self.right_face_actor:
                self.plotter.remove_actor(actor)
            self.right_face_actor.clear()

        if len(self.right_point_labels_actor) != 0:
            for temp_actor in self.right_point_labels_actor:
                self.plotter.remove_actor(temp_actor)
            self.right_point_labels_actor.clear()

        if len(self.right_line_actor) != 0 :
            for temp_actor in self.right_line_actor:
                self.plotter.remove_actor(temp_actor)
            self.right_line_actor.clear()

        if len(self.right_point) != 0:
            self.right_point.clear() 
        self.right_line_points.clear()
        label.setText("Selected points:"+str(len(self.right_point)))

    def calc_distance(self):
        len_left_data = len(self.left_point)
        len_right_data = len(self.right_point)

        if len_left_data == 1 and len_right_data == 1:
            distance._distance_between_points(self)
        
        elif ( len_left_data == 1 and len_right_data ==2 
              ) or ( len_left_data== 2 and len_right_data == 1):
            distance._distance_between_point_and_line(self)
        
        elif ( len_left_data == 1 and len_right_data ==3 
              ) or ( len_left_data== 3 and len_right_data == 1):
            distance._distance_between_point_and_face(self)

        elif len_left_data == 2 and len_right_data ==2:
            distance._distance_between_line_and_line(self)

        elif ( len_left_data == 2 and len_right_data ==3 
              ) or ( len_left_data== 3 and len_right_data == 2):
            distance._distance_between_line_and_face(self)

        elif  len_left_data == 3 and len_right_data ==3 :
           distance._distance_between_face_and_face(self)

        else:
            self.distLabel.setText("Incalculable distance")

    def select_cylinder(self):

        picker = radius.Picker_cylinder(self.plotter,
                    self.mesh, self.cylinderLabel,self.radius_actor,
                                 self.left_point,self.right_point)
        self.plotter.track_click_position(picker, side='right')
        # print()
    
    def clear_all(self):
        self.clear_left_data(self.label1)
        self.clear_right_data(self.label2)

        # self.clear_left_data(self.label)
        # self.clear_right_data(self.label_2)
        self.label.setText("Selected points:"+
                           str(len(self.right_point)))
        self.label_2.setText("Selected points:"+
                             str(len(self.right_point)))
        for temp_actor in self.line_actor:
            self.plotter.remove_actor(temp_actor)
        self.line_actor.clear()

        for temp_actor in self.face_actor:
            self.plotter.remove_actor(temp_actor)
        self.face_actor.clear()

        self.label.setText("Selected points:"+str(len(self.left_point)))
        self.label_2.setText("Selected points:"+str(len(self.left_point)))

        self.label_4.setText("")
        self.label_5.setText("")
        self.distLabel.setText("")
        self.radiusLabel.setText("")
        self.circleLabel.setText("")
        self.cylinderLabel.setText("")

    def calc_angle(self,label):
        len_left_data = len(self.left_point)
        len_right_data = len(self.right_point)
        if len_left_data == 2 and len_right_data ==2:
            angle._angle_between_line_and_line(self,label)
        
        elif ( len_left_data == 2 and len_right_data ==3 
            ) or ( len_left_data== 3 and len_right_data == 2):
            angle._angle_between_line_and_face(self,label)

        elif  len_left_data == 3 and len_right_data ==3 :
            angle._angle_between_face_and_face(self,label)
    
    def calc_area(self,label):
        area = self.mesh.area
        label.setText("Area is "+ str(area))

    def calc_volume(self,label):
        volume = self.mesh.volume
        label.setText("Volume is "+ str(volume))


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle('Fusion')
    window =  MyMainWindows()
    window.show()
    sys.exit(app.exec_())
    

