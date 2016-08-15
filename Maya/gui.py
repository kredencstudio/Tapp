from Qt import QtWidgets

import maya.cmds as cmds
# import maya.OpenMayaUI as omui

import Tapp.Maya.lighting.gui as lighting
reload(lighting)
# import Tapp.Maya.animation.gui as animation
# reload(animation)
import Tapp.Maya.rigging.gui as rigging
reload(rigging)
import Tapp.Maya.modelling.gui as modelling
reload(modelling)



def maya_main_window():
    """Return Maya's main window"""
    for obj in QtWidgets.qApp.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


class Window(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        QtWidgets.QDialog.__init__(self, parent)

        self.setObjectName('tappDialog')

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_tabs = QtWidgets.QTabWidget()
        self.main_layout.addWidget(self.main_tabs)

        self.main_tabs.addTab(modelling.Window(), 'Modelling')
        self.main_tabs.addTab(rigging.Window(), 'Rigging')
        # self.main_tabs.addTab(animation.Window(), 'Animation')
        self.main_tabs.addTab(lighting.Window(), 'Lighting')

    def show(self):
        #delete previous ui
        if cmds.dockControl('tappWindow', exists=True):
            cmds.deleteUI('tappWindow')

        #creating ui
        win = Window()
        minSize = win.minimumSizeHint()
        cmds.dockControl('tappWindow', content='tappDialog', area='right',
                         label='Tapp', width=minSize.width())
