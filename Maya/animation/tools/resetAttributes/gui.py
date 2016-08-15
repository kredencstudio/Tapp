from Qt import QtWidgets


import maya.cmds as cmds
import maya.OpenMayaUI as omui

from .resources import dialog as dialog


def maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')

class Window(QtWidgets.QMainWindow, dialog.Ui_MainWindow):

    def __init__(self, parent=maya_main_window()):
        super(Window, self).__init__(parent)
        self.setupUi(self)

        self.modify_dialog()

        self.create_connections()

    def modify_dialog(self):

        pass

    def create_connections(self):

        self.pushButton.released.connect(self.pushButton_released)

    def pushButton_released(self):

        translation = self.translation_checkBox.isChecked()
        rotation = self.rotation_checkBox.isChecked()
        scale = self.scale_checkBox.isChecked()
        userAttrs = self.extraAttributes_checkBox.isChecked()

        self.resetSelection(translation, rotation, scale, userAttrs)

    def resetAttribute(self, node, attr):

        #reset attributes to default if keyable
        if cmds.attributeQuery(attr, node=node, keyable=True):
            values = cmds.attributeQuery(attr, node=node, listDefault=True)

            try:
                cmds.setAttr(node + '.' + attr, *values)
            except:
                pass

    def resetAttributes(self, node, translation=True, rotation=True,
                       scale=True, userAttrs=True):

        if translation:
            self.resetAttribute(node, 'tx')
            self.resetAttribute(node, 'ty')
            self.resetAttribute(node, 'tz')

        if rotation:
            self.resetAttribute(node, 'rx')
            self.resetAttribute(node, 'ry')
            self.resetAttribute(node, 'rz')

        if scale:
            self.resetAttribute(node, 'sx')
            self.resetAttribute(node, 'sy')
            self.resetAttribute(node, 'sz')

        if userAttrs:
            if cmds.listAttr(node, userDefined=True):
                for attr in cmds.listAttr(node, userDefined=True):
                    self.resetAttribute(node, attr)

    def resetSelection(self, translation=True, rotation=True,
                      scale=True, userAttrs=True):

        #undo enable
        cmds.undoInfo(openChunk=True)

        #getting selection
        sel = cmds.ls(sl=True)

        #zero nodes
        if len(sel) >= 1:
            for node in cmds.ls(sl=True):
                self.resetAttributes(node, translation, rotation,
                               scale, userAttrs)

            #revert selection
            cmds.select(sel)
        else:
            cmds.warning('No nodes select!')

        cmds.undoInfo(closeChunk=True)


def show():
    win = Window()
    win.show()
