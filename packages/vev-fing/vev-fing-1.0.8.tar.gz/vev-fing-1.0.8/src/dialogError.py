from PyQt5 import QtWidgets,uic, QtCore
from PyQt5.QtGui import QPixmap

path_buttons='src/buttons_and_background/'
class dError(QtWidgets.QDialog):
    def __init__(self, errorMessage,parent=None):
        super(dError, self).__init__()
        uic.loadUi('src/ui_files/dialogError.ui', self)
        self._flag = False
        self.pushButton.clicked.connect(self.closeWindow)
        self.pushButton.setStyleSheet("QPushButton{border-image:url("+path_buttons+"Ok.png);}")
        self.pushButton.setToolTip("Click to close window")
        self.errorText.setText(errorMessage)



    def closeWindow(self):
        self.close()
