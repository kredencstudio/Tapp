from . import utils

import os
import webbrowser

import maya.cmds as cmds
import maya.mel as mel

from Qt import QtWidgets

from .resources import dialog
reload(dialog)


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

        self.setObjectName('tapp_modelling')

        self.loadedStyleSheet='QPushButton {color: white;background-color: green}'

        self.posVerts = None
        self.upVert = None

    def create_connections(self):

        self.loadPositionVerts_pushButton.released.connect(self.on_loadPositionVerts_pushButton_released)
        self.loadUpVert_pushButton.released.connect(self.on_loadUpVert_pushButton_released)
        self.create_pushButton.released.connect(self.on_create_pushButton_released)
        self.scatter_pushButton.released.connect(self.on_scatter_pushButton_released)
        self.scatterInfo_pushButton.released.connect(self.on_scatterInfo_pushButton_released)
        self.detachSeparate_pushButton.released.connect(self.on_detachSeparate_pushButton_released)
        self.uvDeluxe_pushButton.released.connect(self.on_uvDeluxe_pushButton_released)
        self.psdImport_pushButton.released.connect(self.on_psdImport_pushButton_released)
        self.instanceAlongCurve_pushButton.released.connect(self.on_instanceAlongCurve_pushButton_released)
        self.rivet_pushButton.released.connect(self.on_rivet_pushButton_released)
        self.plotCurve_pushButton.released.connect(self.on_plotCurve_pushButton_released)
        self.edgesToCurves_pushButton.released.connect(self.on_edgesToCurves_pushButton_released)
        self.curvOnMesh_pushButton.released.connect(self.on_curvOnMesh_pushButton_released)
        self.curveToPoly_pushButton.released.connect(self.on_curveToPoly_pushButton_released)


    def on_uvDeluxe_pushButton_released(self):

        from UVDeluxe import uvdeluxe
        uvdeluxe.createUI()


    def on_loadPositionVerts_pushButton_released(self):

        sel = cmds.ls(selection=True, flatten=True)

        if len(sel) > 0:

            shape = cmds.ls(selection=True, objectsOnly=True)[0]

            if cmds.nodeType(shape) == 'mesh':
                if cmds.polyEvaluate()['vertexComponent'] > 0:

                    verts = []
                    for vert in sel:

                        verts.append(vert)

                    if len(verts) == 2:
                        self.posVerts = verts
                        self.positionVerts_label.setText('Verts loaded!')
                        self.loadPositionVerts_pushButton.setStyleSheet(self.loadedStyleSheet)
                    else:
                        cmds.warning('More or Less than two verts selected. Please select only 2 verts.')
                else:
                    cmds.warning('No verts selected!')
            else:
                cmds.warning('Selection is not a vertex!')
        else:
            cmds.warning('Nothing is selected!')

    def on_loadUpVert_pushButton_released(self):

        sel = cmds.ls(selection=True,flatten=True)

        if len(sel) > 0:

            shape = cmds.ls(selection=True, objectsOnly=True)[0]

            if cmds.nodeType(shape) == 'mesh':
                if cmds.polyEvaluate()['vertexComponent']>0:

                    verts = []
                    for vert in sel:

                        verts.append(vert)

                    self.upVert = verts
                    self.upVert_label.setText('Vert loaded!')
                    self.loadUpVert_pushButton.setStyleSheet(self.loadedStyleSheet)
                else:
                    cmds.warning('No vert selected!')
            else:
                cmds.warning('Selection is not a vertex!')
        else:
            cmds.warning('Nothing is selected!')

    def on_create_pushButton_released(self):

        if self.posVerts != None and self.upVert != None:

            #get check box state
            state = self.locator_checkBox.checkState()

            if state == 0:
                locatorPivot = False
            if state == 2:
                locatorPivot = True

            #get check box state
            state = self.mesh_checkBox.checkState()

            if state == 0:
                meshPivot = False
            if state == 2:
                meshPivot = True

            #execute
            utils.triangulatePivot(self.posVerts, self.upVert, locatorPivot, meshPivot)

        else:
            cmds.warning('Position Verts and Upvector Vert not loaded!')

    def on_scatter_pushButton_released(self):

        melPath = os.path.dirname(__file__) + '/icPolyScatter.mel'
        melPath = melPath.replace('\\', '/')
        mel.eval('source "%s"' % melPath)
        mel.eval('icPolyScatter')

    def on_scatterInfo_pushButton_released(self):

        webbrowser.open('http://www.braverabbit.de/playground/?p=474')

    def on_detachSeparate_pushButton_released(self):

        melPath = os.path.dirname(__file__) + '/detachSeparate.mel'
        melPath = melPath.replace('\\', '/')
        mel.eval('source "%s"' % melPath)
        mel.eval('detachSeparate')

    def on_psdImport_pushButton_released(self):

        melPath = os.path.dirname(__file__) + '/enBuild.mel'
        melPath = melPath.replace('\\', '/')
        mel.eval('source "%s"' % melPath)

    def on_instanceAlongCurve_pushButton_released(self):
        if not cmds.pluginInfo('instanceAlongCurve.py', query=1, loaded=1):
            cmds.loadPlugin('instanceAlongCurve.py', quiet=1)
        mel.eval('instanceAlongCurve')

    def on_rivet_pushButton_released(self):
        melPath = os.path.dirname(__file__) + '/djRivet.mel'
        melPath = melPath.replace('\\', '/')
        mel.eval('source "%s"' % melPath)
        mel.eval('djRivet')

    def on_plotCurve_pushButton_released(self):
        import hart_plotCurve
        hart_plotCurve.plotCurve()

    def on_edgesToCurves_pushButton_released(self):
        melPath = os.path.dirname(__file__) + '/rainCurves.mel'
        melPath = melPath.replace('\\', '/')
        mel.eval('source "%s"' % melPath)
        mel.eval('rainCurvesFromEdges')

    def on_curvOnMesh_pushButton_released(self):
        import gf_curveOnMeshCtx as cmCtx
        reload(cmCtx)
        cmCtx.UI().create()

    def on_curveToPoly_pushButton_released(self):
        melPath = os.path.dirname(__file__) + '/da_curveToPoly.mel'
        melPath = melPath.replace('\\', '/')
        mel.eval('source "%s"' % melPath)
        mel.eval('da_curveToPoly')


def show():
    #closing previous dialog
    for widget in QtGui.QApplication.allWidgets():
        if widget.objectName() == 'tapp_modelling':
            widget.close()

    #showing new dialog
    win = Window()
    win.show()
