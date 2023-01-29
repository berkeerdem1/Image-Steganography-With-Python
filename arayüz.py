from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('projearayüz.ui', self)

        main_title = "test"
        self.setWindowTitle(main_title)


if __name__ == '__main__':
    import sys
    app = QtWidgets. QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
