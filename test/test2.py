import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QToolBox, QGroupBox, QToolButton, QVBoxLayout


class Demo(QToolBox):                                           # 1
    def __init__(self):
        super(Demo, self).__init__()
        self.groupbox_1 = QGroupBox(self)                       # 2
        self.groupbox_2 = QGroupBox(self)
        self.groupbox_3 = QGroupBox(self)

        self.toolbtn_f1 = QToolButton(self)                     # 3
        self.toolbtn_f2 = QToolButton(self)
        self.toolbtn_f3 = QToolButton(self)
        self.toolbtn_m1 = QToolButton(self)
        self.toolbtn_m2 = QToolButton(self)
        self.toolbtn_m3 = QToolButton(self)

        self.v1_layout = QVBoxLayout()
        self.v2_layout = QVBoxLayout()
        self.v3_layout = QVBoxLayout()

        self.addItem(self.groupbox_1, 'Couple One')             # 4
        self.addItem(self.groupbox_2, 'Couple Two')
        self.addItem(self.groupbox_3, 'Couple Three')
        self.currentChanged.connect(self.print_index_func)      # 5

        self.layout_init()
        self.groupbox_init()
        # self.toolbtn_init()

    def layout_init(self):
        self.v1_layout.addWidget(self.toolbtn_f1)
        self.v1_layout.addWidget(self.toolbtn_m1)
        self.v2_layout.addWidget(self.toolbtn_f2)
        self.v2_layout.addWidget(self.toolbtn_m2)
        self.v3_layout.addWidget(self.toolbtn_f3)
        self.v3_layout.addWidget(self.toolbtn_m3)

    def groupbox_init(self):                                    # 6
        self.groupbox_1.setFlat(True)
        self.groupbox_2.setFlat(True)
        self.groupbox_3.setFlat(True)
        self.groupbox_1.setLayout(self.v1_layout)
        self.groupbox_2.setLayout(self.v2_layout)
        self.groupbox_3.setLayout(self.v3_layout)

    def toolbtn_init(self):                                     # 7
        self.toolbtn_f1.setIcon(QIcon('images/f1.ico'))
        self.toolbtn_f2.setIcon(QIcon('images/f2.ico'))
        self.toolbtn_f3.setIcon(QIcon('images/f3.ico'))
        self.toolbtn_m1.setIcon(QIcon('images/m1.ico'))
        self.toolbtn_m2.setIcon(QIcon('images/m2.ico'))
        self.toolbtn_m3.setIcon(QIcon('images/m3.ico'))

    def print_index_func(self):
        couple_dict = {
            0: 'Couple One',
            1: 'Couple Two',
            2: 'Couple Three'
        }
        sentence = 'You are looking at {}.'.format(couple_dict.get(self.currentIndex()))
        print(sentence)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_()) 