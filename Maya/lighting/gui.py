import os

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
import maya.OpenMayaUI as omui

from Qt import QtWidgets
# from shiboken import wrapInstance

from .resources import dialog
from Tapp.Maya.lighting.alembic import utils
import Tapp.Maya.lighting.arnold as mla


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

        self.addRimLight_pushButton.released.connect(self.on_addRimLight_pushButton_released)

        self.exportAlembic_pushButton.released.connect(self.on_exportAlembic_pushButton_released)
        self.importAlembic_pushButton.released.connect(self.on_importAlembic_pushButton_released)
        self.connectAlembic_pushButton.released.connect(self.on_connectAlembic_pushButton_released)

        self.arnoldLoad_pushButton.released.connect(self.on_arnoldLoad_pushButton_released)

        self.arnoldAddProxyMat_pushButton.setEnabled(False)
        self.arnoldDeleteProxyMat_pushButton.setEnabled(False)
        self.transferShading_pushButton.released.connect(self.transferShading_pushButton_released)
        self.autoAsignShaders_pushButton.setEnabled(False)

        self.arnoldConvertToStandard_pushButton.released.connect(self.convert_to_arnoldMat)
        self.arnoldConvertToAlSurface_pushButton.released.connect(self.convert_to_arnoldMat)

        self.idRed_pushButton.released.connect(self.on_arnoldIdColor_pushButton_released)
        self.idGreen_pushButton.released.connect(self.on_arnoldIdColor_pushButton_released)
        self.idBlue_pushButton.released.connect(self.on_arnoldIdColor_pushButton_released)
        self.arnoldAddObjID_pushButton.released.connect(self.on_arnoldMask_pushButton_released)
        self.arnoldRemObjID_pushButton.released.connect(self.on_arnoldRemObjID_pushButton_released)
        self.arnoldAddShaderID_pushButton.released.connect(self.on_arnoldRebuildMask_pushButton_released)

        self.arnoldSubdivision_none.released.connect(self.on_arnoldSubdivision_pushButton_released)
        self.arnoldSubdivision_catclark.released.connect(self.on_arnoldSubdivision_pushButton_released)
        self.arnoldSubdivision_linear.released.connect(self.on_arnoldSubdivision_pushButton_released)

        self.arnoldOpaque_checkBox.setEnabled(False)
        self.arnoldSelfShad_checkBox.setEnabled(False)
        self.arnoldInDiff_checkBox.setEnabled(False)
        self.arnoldInSpec_checkBox.setEnabled(False)
        self.arnoldMatte_checkBox.setEnabled(False)

        self.arnoldAddAttrs_pushButton.released.connect(self.on_arnoldAddAttrs_pushButton_released)

        self.alLightGroup_1_pushButton.released.connect(self.set_light_group)
        self.alLightGroup_2_pushButton.released.connect(self.set_light_group)
        self.alLightGroup_3_pushButton.released.connect(self.set_light_group)
        self.alLightGroup_4_pushButton.released.connect(self.set_light_group)
        self.alLightGroup_5_pushButton.released.connect(self.set_light_group)
        self.alLightGroup_6_pushButton.released.connect(self.set_light_group)
        self.alLightGroup_7_pushButton.released.connect(self.set_light_group)
        self.alLightGroup_8_pushButton.released.connect(self.set_light_group)


    def transferShading_pushButton_released(self):
        import alembic_mtl
        amtl = alembic_mtl.AssignMtlCtl()
        amtl.selectAllCtl()

    def on_exportAlembic_pushButton_released(self):

        utils.Export()

    def on_importAlembic_pushButton_released(self):
        reload(utils)
        utils.Import()

    def on_connectAlembic_pushButton_released(self):
        reload(utils)
        sel = pm.ls(sl=True)
        utils.Connect(sel[0], sel[1])

    def on_addRimLight_pushButton_released(self):

        mla.addRimRamp()

    def on_arnoldSubdivision_pushButton_released(self):

        reload(mla)
        iterations = self.arnoldSubdivision_spinBox.value()
        if self.sender().text() == 'None':
            aiSubdType = 0
        elif self.sender().text() == 'Catclark':
            aiSubdType = 1
        elif self.sender().text() == 'Linear':
            aiSubdType = 1

        mla.aiSetSubd(aiSubdType)
        mla.aiSetIter(iterations)

    def on_arnoldIdColor_pushButton_released(self):

        color = self.sender().text().lower()
        layer = self.arnoldIdLayer_spinBox.value()

        mla.setIdColor(color, layer)

    def on_arnoldRemObjID_pushButton_released(self):

        mla.clearIDs()

    def on_arnoldMask_pushButton_released(self):

        mla.Mask()

    def on_arnoldRebuildMask_pushButton_released(self):

        mla.MaskFlush()
        mla.MaskBuild()

    def convert_to_arnoldMat(self):

        import Tapp.Maya.lighting.mayaMat2Ai as m2Ai
        matType = self.sender().text()
        proxy = self.leaveProxy_checkBox.isChecked()
        print proxy
        m2Ai.convert(matType, proxy)

    def set_arnoldAttr(self):

        proxy = self.leaveProxy_checkBox.isChecked()
        print proxy
        m2Ai.convert(matType, proxy)

    def set_light_group(self):

        reload(mla)
        lightGroup = self.sender().text()
        mla.addToLightGroup(lightGroup)


    def on_arnoldAddAttrs_pushButton_released(self):

        import Tapp.Maya.lighting.aiCreateAttr as aiAttr
        aiAttr.windowADD()

    def on_arnoldLoad_pushButton_released(self):

        reload(mla)
        mla.loadArnold()

def show():
    #closing previous dialog
    for widget in QtWidgets.qApp.allWidgets():
        if widget.objectName() == 'tapp_lighting':
            widget.close()

    #showing new dialog
    win = Window()
    win.show()
