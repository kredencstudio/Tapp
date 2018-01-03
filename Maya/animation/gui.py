from . import setsSelector, playblastQueue, utils
from .resources import dialog
reload(dialog)
from ..utils import ZvParentMaster

import os
import webbrowser

from Qt import QtGui, QtWidgets

import maya.OpenMayaUI as omui
import maya.cmds as cmds
import maya.mel as mel


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

        self.create_connections()

    def modify_dialog(self):

        self.setObjectName('tapp_animation')

        layout = self.central_verticalLayout


        #adding Sets Selector to dialog
        layout.addWidget(setsSelector.Window())


    def create_connections(self):

        self.zvParentMaster_pushButton.released.connect(
                                    self.zvParentMaster_pushButton_released)
        self.zvChain_pushButton.released.connect(
                                             self.zvChain_pushButton_released)
        self.zvParentMasterHelp_pushButton.released.connect(
                                self.zvParentMasterHelp_pushButton_released)

        self.keyCleanUp_pushButton.released.connect(
                                        self.keyCleanUp_pushButton_released)
        self.keyCleanUpHelp_pushButton.released.connect(
                                    self.keyCleanUpHelp_pushButton_released)

        self.changeRotationOrder_pushButton.released.connect(
                                 self.changeRotationOrder_pushButton_released)
        self.changeRotationOrderHelp_pushButton.released.connect(
                             self.changeRotationOrderHelp_pushButton_released)

        self.localizeImagePlane_pushButton.released.connect(
                                self.localizeImagePlane_pushButton_released)

        self.playblastQueue_pushButton.released.connect(
                                               self.playblastQueue_released)

    def playblastQueue_released(self):

        win = playblastQueue.Window()
        win.show()

    def zvParentMaster_pushButton_released(self):

        ZvParentMaster.ZvParentMaster()

    def zvChain_pushButton_released(self):

        #undo enable
        cmds.undoInfo(openChunk=True)

        ZvParentMaster.attach_chain()

        cmds.undoInfo(closeChunk=True)

    def zvParentMasterHelp_pushButton_released(self):

        webbrowser.open(
                'http://www.creativecrash.com/maya/script/zv-parent-master')

    def localizeImagePlane_pushButton_released(self):

        import Tapp.Maya.animation.utils.imageplane as ip

        ip.localizeImagePlane()

    def keyCleanUp_pushButton_released(self):

        cmds.undoInfo(openChunk=True)

        #execute redundant keys script
        path = os.path.dirname(utils.__file__).replace('\\', '/')

        mel.eval('source "' + path + '/deleteRedundantKeys.mel"')
        mel.eval('llDeleteRedundantKeys;')

        #deleting static channels in scene or on selected object
        sel = cmds.ls(selection=True)

        if len(sel) > 0:
            cmds.delete(staticChannels=True)
        else:
            cmds.delete(staticChannels=True, all=True)

        cmds.undoInfo(closeChunk=True)

    def keyCleanUpHelp_pushButton_released(self):

        msg = 'This cleans any static channels and redundant keys.\n'
        msg += 'If nothing is selected, everything in the scene gets cleaned.'

        cmds.confirmDialog(title='Key Clean Up Info', message=msg,
                           defaultButton='OK')

    def changeRotationOrder_pushButton_released(self):

        path = os.path.dirname(utils.__file__)

        #sourcing zoo utils
        melPath = path + '/zooUtils.mel'
        melPath = melPath.replace('\\', '/')
        mel.eval('source "%s"' % melPath)

        #sourcing zoo change
        melPath = path + '/zooChangeRoo.mel'
        melPath = melPath.replace('\\', '/')
        mel.eval('source "%s"' % melPath)

        mel.eval('zooChangeRoo %s' %
                 self.tools_changeRotationOrder_comboBox.currentText())

    def changeRotationOrderHelp_pushButton_released(self):

        webbrowser.open(
                    'http://www.creativecrash.com/maya/script/zoochangeroo')
