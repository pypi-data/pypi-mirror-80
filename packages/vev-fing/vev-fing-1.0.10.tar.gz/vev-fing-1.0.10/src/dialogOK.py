from PyQt5 import QtWidgets,uic

path_buttons='src/buttons_and_background/'
class dOK(QtWidgets.QDialog):
    def __init__(self, errorMessage,parent=None):
        super(dOK, self).__init__()
        uic.loadUi('src/ui_files/dialogOK.ui', self)
        self._flag = False
        self.pushButton.clicked.connect(self.closeWindow)
        self.pushButton.setStyleSheet("QPushButton{border-image:url("+path_buttons+"Ok.png);}")
        self.pushButton.setToolTip("Click to close window")
        self.text.setText(errorMessage)
    def closeWindow(self):
        self.close()
