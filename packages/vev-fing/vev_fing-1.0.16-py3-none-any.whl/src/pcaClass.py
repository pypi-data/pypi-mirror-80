import numpy as np
import pandas as pd
from PIL import Image
from sklearn.decomposition import PCA
import matplotlib
import os
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, uic
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.PlotEntropyPosition import plotEntropyPosition, plotEntropiesPosition


pathPip=str(os.path.dirname(Image.__file__)).split('PIL')[0]

class FigurePCA(FigureCanvas):

    def __init__(self, dfPuntosPCA, pcaVector, infoDF, nameExps,dfs, parent, width=5, height=4, dpi=100):

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.parent = parent

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.dfPuntosPCA = dfPuntosPCA
        self.infoDF = infoDF
        self.pcaVector = pcaVector
        self.nameExps = nameExps
        self.dfsAux = dfs
        self.fig = fig
        self.aux = []
        self.compute_initial_figure()
        self.name = ''
        self._flag = False

    def updatePCA(self,dfPuntosPCA,pcaVector,infoDF,nameExps,dfs):
        self.dfPuntosPCA = dfPuntosPCA
        self.pcaVector = pcaVector
        self.infoDF = infoDF
        self.nameExps = nameExps
        self.dfsAux = dfs
        self.axes.cla()
        self.compute_initial_figure()

    def compute_initial_figure(self):

        strains = self.dfPuntosPCA.Strain.unique()

        self.fig.canvas.mpl_connect('button_press_event', self.check_click)
        self.aux = self.axes.scatter(self.pcaVector[0, :], self.pcaVector[1, :], marker='o', c="grey", alpha=0.2)
        for s in strains:
            d = self.dfPuntosPCA.loc[self.dfPuntosPCA['Strain'] == s]
            x = d.PCA_1 / 60
            y = d.PCA_2 / 60
            self.axes.scatter(x, y, label=s)
        self.axes.set_xlabel('X1')
        self.axes.set_ylabel('X2')
        self.axes.legend()
        title = 'Distribucion coeficientes de componentes principales posicion '
        plt.suptitle(title, fontsize=16)
        self.axes.grid(True)
        self.draw()

    def find_nearest(self, points, value):
        arrayAux = np.asarray(points)
        idx = (np.abs(arrayAux - value)).argmin()
        return idx

    def check_click(self, event):
        if event.inaxes == self.axes:
            cont, ind = self.aux.contains(event)
            if cont:
                self.onclick(event)


    def onclick(self, event):
        ix, iy = event.xdata, event.ydata
        indx = self.find_nearest(self.pcaVector[0,], ix)
        exp = self.infoDF[0,]
        experiment = exp[indx]
        experimentAux = experiment.split(',')
        position = experimentAux[3]
        plotEntropiesPosition(int(position), self.dfsAux)
        self.name = pathPip+'src/plot_images/Entropy_' + position + '.png'
        img = Image.open(self.name)
        titleAux = pathPip+"plot_images/Entropy for position " + position
        img.show(title=titleAux)
