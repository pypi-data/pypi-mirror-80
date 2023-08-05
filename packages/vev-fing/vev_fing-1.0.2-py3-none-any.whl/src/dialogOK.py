from PyQt5 import QtWidgets,uic

path_buttons='buttons_and_background/'
class dOK(QtWidgets.QDialog):
    def __init__(self, errorMessage,parent=None):
        super(dOK, self).__init__()
        uic.loadUi('ui_files/dialogOK.ui', self)
        self._flag = False
        self.pushButton.clicked.connect(self.closeWindow)
        self.pushButton.setStyleSheet("QPushButton{border-image:url("+path_buttons+"Ok.png);}")
        self.pushButton.setToolTip("Click to close window")
        self.text.setText(errorMessage)
    def closeWindow(self):
        self.close()

"""    def scale_image(self,size):
        imageBack = QImage(path_buttons+'baseBackground.png')
        imageBack= imageBack.scaled(size,QtCore.Qt.KeepAspectRatio)
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(imageBack))
        self.setPalette(palette)

    def resizeEvent(self, e):
        if not self._flag:
            self._flag = True
            self.scale_image(e.size())
            QtCore.QTimer.singleShot(150, lambda: setattr(self, "_flag", False))
        super().resizeEvent(e)"""