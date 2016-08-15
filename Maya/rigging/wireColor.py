import pymel.core as pm
import maya.OpenMayaUI as omui
from Qt import QtGui, QtCore, QtWidgets


def maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


class MPalette(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(MPalette, self).__init__(parent)
        self._color = -1
        self._styleSheet = ""
        self.setupUi()
        for i, b in enumerate(self.buttons):
            self.setButtonColor(
                b, [x * 255 for x in pm.colorIndex(i + 1, q=True)])
            b.clicked.connect(lambda index=i + 1: self.accept(index))

    def setupUi(self):
        self.setWindowTitle("ColorPicker")
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.buttons = list()
        for i in range(31):
            btn = QtWidgets.QPushButton(self)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                           QtWidgets.QSizePolicy.Maximum)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(
                btn.sizePolicy().hasHeightForWidth())
            btn.setSizePolicy(sizePolicy)
            btn.setMaximumSize(QtCore.QSize(25, 25))
            btn.setText(str(i + 1))
            self.gridLayout.addWidget(btn, int(i / 8), i % 8, 1, 1)
            self.buttons.append(btn)

    def setButtonColor(self, button, color):
        s = "background-color: rgb({0}, {1}, {2});".format(*color)
        button.setStyleSheet(s)

    def accept(self, index=None):
        self._color = index
        super(MPalette, self).accept()

    @classmethod
    def getColor(cls, parent):
        palette = cls(parent)
        palette.exec_()
        return palette._color


def Selection():
    index = MPalette.getColor(parent=maya_main_window())

    for node in pm.ls(selection=True):
        node.overrideEnabled.set(True)
        node.overrideColor.set(index)
