from PyQt5 import QtCore, QtGui,QtWidgets
import sys 

class MyClass(object):
    def __init__(self, arg):
        super(MyClass, self).__init__()
        self.arg = arg        

class myWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(myWindow, self).__init__(parent)
        # QtWidgets.resize(300,200)
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.addItems([str(x) for x in [3,4,5]])


        slotLambda = lambda text: self.indexChanged_lambda(text,"123")
        self.comboBox.currentIndexChanged.connect(slotLambda)

    # @QtCore.pyqtSlot(str)
    def indexChanged_lambda(self,text,str1):
        print ('lambda:', text, str1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('myApp')
    dialog = myWindow()
    dialog.resize(300,200)
    dialog.show()
    sys.exit(app.exec_())