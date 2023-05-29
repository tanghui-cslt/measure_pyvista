import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolBox, QPushButton, QFrame


class QmyWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)  # 调用父类的构造函数，创建QWidget窗体
        self.setupUi()

    def setupUi(self):
        """页面初始化"""
        # 设置窗体大小及标题
        self.resize(500, 400)
        self.setWindowTitle("QToolBox组件示例")
        # 创建布局
        self.main_layout = QVBoxLayout()

        # QVBoxLayout组件定义
        self.toolBox = QToolBox()   # 定义工具箱
        self.setupTool1()           # 初始化构造的工具集1
        self.setupTool2()           # 初始化构造的工具集2
        # QVBoxLayout组件设置
        self.toolBox.setCurrentIndex(1)
        self.toolBox.setItemIcon(0, QIcon("logo.png"))
        self.toolBox.setItemIcon(1, QIcon("logo.png"))
        # QVBoxLayout绑定信号
        self.toolBox.currentChanged.connect(self.on_toolBox_currentChanged)

        # 将组件添加到布局中
        self.main_layout.addWidget(self.toolBox)
        # 为窗体添加布局
        self.setLayout(self.main_layout)

    def setupTool1(self):
        """槽函数"""
        # 1.创建一个frame容器
        frame = QFrame()
        # 2.创建垂直布局实例
        layout = QVBoxLayout()
        # 3.创建子组件，如按钮组件
        button1 = QPushButton("Button1")
        button2 = QPushButton("Button2")
        # 4.为布局添加子组件
        layout.addWidget(button1)
        layout.addWidget(button2)
        # 将布局添加到frame容器
        frame.setLayout(layout)
        self.toolBox.addItem(frame, "Tool 1")

    def setupTool2(self):
        """槽函数"""
        # 1.创建一个frame容器
        frame = QFrame()
        # 2.创建垂直布局实例
        layout = QVBoxLayout()
        # 3.创建子组件，如按钮组件
        button3 = QPushButton("Button3")
        button4 = QPushButton("Button4")
        # 4.为布局添加子组件
        layout.addWidget(button3)
        layout.addWidget(button4)
        # 将布局添加到frame容器
        frame.setLayout(layout)
        self.toolBox.addItem(frame, "Tool 2")

    def on_toolBox_currentChanged(self, index):
        """槽函数"""
        print("当前切换的工具集为：{}".format(str(index)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myMain = QmyWidget()
    myMain.show()
    sys.exit(app.exec_())