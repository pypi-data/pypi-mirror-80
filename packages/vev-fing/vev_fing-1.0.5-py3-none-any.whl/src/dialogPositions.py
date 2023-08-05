from PyQt5 import QtWidgets,uic
from src.dialogError import dError

class valuesPositions(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(valuesPositions, self).__init__()
        uic.loadUi('src/ui_files/dialogPositions.ui', self)
        self.pushButton.clicked.connect(self.setParameters)
        self.fvpValue=774
        self.lvpValue=7332
    def setParameters(self):

        fvp = self.FVP.toPlainText()
        lvp = self.LVP.toPlainText()
        try:
            if fvp == '':
                fvp = 0
            if lvp == '':
                lvp = 0
            self.fvpValue = int(fvp)
            self.lvpValue = int(lvp)
            self.close()
        except:
            de = dError("Error: Enter only integers")
            de.exec()

    def getFVP(self):
        return self.fvpValue
    def getLVP(self):
        return self.lvpValue