from Qt import QtWidgets

import maya.cmds as cmds
import maya.OpenMayaUI as omui

from .resources import dialog
reload(dialog)

'''
import os

#rebuild ui
import Tapp.System.pyside.compileUi as upc
uiPath = os.path.dirname(dialog.__file__) + '/dialog.ui'
upc.compileUi(uiPath)
reload(dialog)
'''


def maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


class Window(QtWidgets.QMainWindow, dialog.Ui_MainWindow):

    def __init__(self, parent=maya_main_window()):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        self.modify_dialog()

        self.refresh()

        self.create_connections()

    def modify_dialog(self):

        pass

    def refresh(self):

        self.listWidget.clear()

        #populate list
        if self.getSets():
            self.listWidget.addItems(self.getSets())

    def create_connections(self):

        self.listWidget.itemSelectionChanged.connect(
                                     self.on_listWidget_itemSelectionChanged)

        self.pushButton.released.connect(self.on_pushButton_released)

    def on_pushButton_released(self):

        self.refresh()

    def on_listWidget_itemSelectionChanged(self):

        members = []
        #getting members of sets
        if self.listWidget.selectedItems():

            for item in self.listWidget.selectedItems():

                members.extend(cmds.listConnections(item.text() +
                                                     '.dagSetMembers'))

        if members:
            cmds.select(members, toggle=self.checkBox.isChecked())
        else:
            cmds.select(cl=True)

    def getSets(self):

        objectSets = []
        for node in cmds.ls(transforms=True):

            sets = cmds.listSets(object=node)
            if sets:
                objectSets.extend(sets)

        return list(set(objectSets))


def show():
    win = Window()
    win.show()
