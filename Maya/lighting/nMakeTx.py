# ##################################################################################
#                                        nMakeTx
#                                 Luca Fiorentini 2013
#                               luca.fiorentini@gmail.com
#                                         v1.0.1
# ##################################################################################
#
# To call the script type in a python tab:
# import nMakeTx
# nMakeTx.Main()
# 
# ##################################################################################
#                                    ChangeLog
# ##################################################################################
# > nMakeTx 1.0.1
#  
# *Fixed path handling to be able to process spaces
# *Fixed error on cancelling browser window
# ##################################################################################
# > nMakeTx 1.0.0
#  
# *First release
# ##################################################################################

import maya.cmds as mc
import os
import maya.mel 
import time
import datetime
import re

from subprocess import call
from maya.OpenMaya import MGlobal

class Main():
    def __init__(self):
        self.name = 'nMakeTxMainUi'
        self.title = 'nMakeTx'
        self.mayaVersion = maya.mel.eval('getApplicationVersionAsFloat')
        self.widgetHeight = 24
        self.fieldLenght = 80
        self.checkBoxLenght = 20
        self.simpleCheckBoxes = []
        self.intCheckBoxes = []
        self.doubleIntCheckBoxes = []
        self.floatCheckBoxes = []
        self.enumCheckBoxes = []
        self.doubleEnumCheckBoxes = []
        
        if not mc.optionVar(q='nMakeTx_makeTxPath'):
            mc.optionVar(sv=['nMakeTx_makeTxPath',    'c:/solidangle/mtoadeploy/%s/bin' % self.mayaVersion])
        if not mc.optionVar(q='nMakeTx_convertOption'):
            mc.optionVar(iv=['nMakeTx_convertOption', 0])
        
        
        self.makeTxPath = mc.optionVar(q='nMakeTx_makeTxPath')
        self.convertBehavior = mc.optionVar(q='nMakeTx_convertOption')
                
        # Begin creating the UI
        if (mc.window(self.name, q=1, exists=1)):
            mc.deleteUI(self.name)
        
        self.window = mc.window(self.name, title=self.title, menuBar=False, s=False)

        self.mainWindowLayout = mc.columnLayout(adj=1)

        self.optionLayout = mc.columnLayout(adj=1, p=self.mainWindowLayout)
        mc.text(l='Convert any texture file to .tx', h=35, bgc=[.125,.125,.125], p=self.optionLayout)
        mc.text(l='', p=self.optionLayout)
        
        self.pathTextField = mc.textFieldButtonGrp('myPathTextField', label='makeTx.exe path:', buttonLabel='Browse', fileName=self.makeTxPath, buttonCommand=Callback(self.browse, 'myPathTextField'), changeCommand=self.saveOptions, cw=[2, 350], w=600, p=self.optionLayout)
        self.textureFrom = mc.radioButtonGrp(label='Use textures from:', labelArray2=['Current scene', 'Folder'], numberOfRadioButtons=2, onc=Callback(self.switchManage, 'myTextureFolderField'), sl=1, vr=False, p=self.optionLayout)
        self.texturePathTextField = mc.textFieldButtonGrp('myTextureFolderField', label='Texture folder', buttonLabel='Browse', fileName='', cw=[2, 350], w=600, buttonCommand=Callback(self.browse, 'myTextureFolderField'), manage=False, p=self.optionLayout)
        self.convertBehaviorRadioButton = mc.radioButtonGrp(label='Convert options:', labelArray3=['Only not existing', 'Overwrite older', 'Overwrite all'], numberOfRadioButtons=3, vr=True, sl=self.convertBehavior + 1, cc=self.saveOptions, p=self.optionLayout)
        mc.text(l='', p=self.optionLayout)
        
        #EXTRA FLAGS
        self.flagLayout = mc.frameLayout( label='Extra flags:', borderStyle='etchedOut', cll=True, cl=True, w=220, p=self.optionLayout)
        self.form = mc.rowColumnLayout(nc=2, p=self.flagLayout, cw=[(1, 300), (2, 300)])
        
        self.simpleCheckWidget('verbose', '-v')
        self.simpleCheckIntFieldWidget('number_of_threads', '--threads')
        self.simpleCheckIntFieldWidget('number_of_channels', '--nchannels')
        self.simpleOptionMenuWidget('output_data_format', '-d', 'uint8', 'sint8', 'uint16', 'sint16', 'half', 'float')
        self.doubleCheckIntFieldWidget('tile_size', '--tile')
        self.simpleCheckWidget('use_planarconfig_separate', '--separate')
        self.simpleCheckFloatFieldWidget('field_of_view', '--fov')
        self.simpleCheckFloatFieldWidget('frame_aspect_ratio', '--fovcot')
        self.simpleCheckWidget('resize', '--resize')
        self.simpleOptionMenuWidget('resize_filter', '--filter', 'box', 'triangle', 'gaussian', 'catrom', 'blackman-harris', 'sinc', 'lanczos3', 'radial-lanczos3', 'mitchell', 'bspline', 'disk')
        self.simpleOptionMenuWidget('wrap', '--wrap', 'black', 'clamp', 'periodic', 'mirror')
        self.simpleOptionMenuWidget('s_wrap', '--swrap', 'black', 'clamp', 'periodic', 'mirror')
        self.simpleOptionMenuWidget('t_wrap', '--twrap', 'black', 'clamp', 'periodic', 'mirror')
        self.simpleCheckWidget('no_mip_map', '--nomipmap')
        self.simpleCheckWidget('check_NaN', '--checknan')
        # self.simpleOptionMenuWidget('fix_NaN', '--fixnan', 'none', 'black', 'box3')
        self.simpleCheckWidget('embed_hash', '--hash')
        self.simpleCheckWidget('embed_Prman_metadata', '--prman-metadata')
        self.simpleCheckWidget('one_tile_from_costant_color', '--constant-color-detect')
        self.simpleCheckWidget('one_channel_from_monochrome', '--monochrome-detect')
        # self.simpleCheckWidget('drop_alpha_channel', '--opaque-detect')
        self.simpleCheckWidget('create_shadowMap', '--shadow')
        self.simpleCheckWidget('create_lat_long_env_map', '--envlatl')
        self.simpleCheckWidget('create_cubic_env_map', '--envcube')
        self.simpleCheckWidget('use_Prman_safe_settings', '--prman')
        self.simpleCheckWidget('use_Oiio_optimized_settings', '--oiio')
        self.doubleCheckAttrEnumWidget('colorspace_transform', '--colorconvert', 'aces', 'raw', 'adx10', 'adx16', 'slogf35', 'slogf65_3200', 'slogf65_5500', 'logc', 'log', 'rrt_srgb', 'rrt_rec709', 'rrt_p3dci', 'rrt_p3d60', 'rrt_xyz', 'lnf', 'lnh', 'ln16', 'lg16', 'lg10', 'lg8', 'lgf', 'gn16', 'gn10', 'gn8', 'gnf', 'vd16', 'vd8', 'vd10', 'vdf', 'hd10', 'dt8', 'dt16', 'cpf', 'nc8', 'nc10', 'nc16', 'ncf', 'sRGB', 'srgb8', 'p3dci8', 'xyz16')
        
        # OVERRIDES
        mc.checkBox('use_Oiio_optimized_settingsCheckBox', e=True, v=True)

        # PROGRESS BAR LAYOUT
        self.progressLayout = mc.columnLayout(adj=True, manage=False, p=self.mainWindowLayout)
        self.progressControl = mc.progressBar(h=30, p=self.progressLayout)
        mc.rowLayout(nc=2, p=self.progressLayout, adj=1, cw1=140)
        self.currentNumberText = mc.text(l='Loading files', align='left')
        self.currentFileText = mc.text(l='', align='right')
        
        # CONVERT LAYOUT
        self.buttonLayout = mc.columnLayout(adj=True, p=self.mainWindowLayout)
        okButton = mc.button(l='Convert', c=self.convert, p=self.buttonLayout, w=100)
        
        mc.showWindow(self.window)
        
    def simpleCheckWidget(self, myLabel, flag):
        self.tempLayout = mc.rowLayout(nc=2, h=self.widgetHeight, p=self.form)
        myCheckBox = mc.checkBox('%sCheckBox' % myLabel, ann=flag, l='', w=self.checkBoxLenght, p=self.tempLayout)
        mc.text('%sText' % myLabel, l=' '.join(myLabel.split('_')), p=self.tempLayout)        
        self.simpleCheckBoxes.append(myLabel)

    def simpleCheckIntFieldWidget(self, myLabel, flag):
        self.tempLayout = mc.rowLayout(nc=3, h=self.widgetHeight, p=self.form)
        myCheckBox = mc.checkBox('%sCheckBox' % myLabel, l='', w=self.checkBoxLenght, ann=flag, cc=Callback(self.activateWidget, '%sIntField' % myLabel), p=self.tempLayout)
        mc.text('%sText' % myLabel, l=' '.join(myLabel.split('_')), w=150, align='left', p=self.tempLayout)
        mc.intField('%sIntField' % myLabel, w=self.fieldLenght, p=self.tempLayout, enable=False)
        self.intCheckBoxes.append(myLabel)

    def simpleCheckFloatFieldWidget(self, myLabel, flag):
        self.tempLayout = mc.rowLayout(nc=3, h=self.widgetHeight, p=self.form)
        myCheckBox = mc.checkBox('%sCheckBox' % myLabel, l='', w=self.checkBoxLenght, ann=flag, cc=Callback(self.activateWidget, '%sFloatField' % myLabel), p=self.tempLayout)
        mc.text('%sText' % myLabel, l=' '.join(myLabel.split('_')), w=150, align='left', p=self.tempLayout)
        mc.floatField('%sFloatField' % myLabel, w=self.fieldLenght, p=self.tempLayout, enable=False)
        self.floatCheckBoxes.append(myLabel)

    def doubleCheckIntFieldWidget(self, myLabel, flag):
        self.tempLayout = mc.rowLayout(nc=4, h=self.widgetHeight, p=self.form)
        myCheckBox = mc.checkBox('%sCheckBox' % myLabel, l='', ann=flag, w=self.checkBoxLenght, cc=Callback(self.activateWidget, '%sIntFieldX' % myLabel, '%sIntFieldY' % myLabel), p=self.tempLayout)
        mc.text('%sText' % myLabel, l=' '.join(myLabel.split('_')), w=150, align='left', p=self.tempLayout)
        mc.intField('%sIntFieldX' % myLabel, p=self.tempLayout, enable=False, w=self.fieldLenght/2)
        mc.intField('%sIntFieldY' % myLabel, p=self.tempLayout, enable=False, w=self.fieldLenght/2)
        self.doubleIntCheckBoxes.append(myLabel)
        
    def simpleCheckAttrEnumWidget(self, myLabel, flag, *attrs):
        myString = []
        for i, attr in enumerate(attrs):
            myString.append((i, attr))
        self.tempLayout = mc.rowLayout(nc=3, h=self.widgetHeight, p=self.form)
        myCheckBox = mc.checkBox('%sCheckBox' % myLabel, l='', w=20, ann=flag, cc=Callback(self.activateWidget, '%sAttrEnum' % myLabel), p=self.tempLayout)
        mc.text('%sText' % myLabel, l=' '.join(myLabel.split('_')), w=150, align='left', p=self.tempLayout)
        mc.attrEnumOptionMenu('%sAttrEnum' % myLabel, l='', ei=myString, enable=False, w=140, p=self.tempLayout)
        self.enumCheckBoxes.append(myLabel)        
        
    def simpleOptionMenuWidget(self, myLabel, flag, *attrs):
        myString = []
        self.tempLayout = mc.rowLayout(nc=3, h=self.widgetHeight, p=self.form)
        myCheckBox = mc.checkBox('%sCheckBox' % myLabel, l='', w=20, ann=flag, cc=Callback(self.activateWidget, '%sOptionMenu' % myLabel), p=self.tempLayout)
        mc.text('%sText' % myLabel, l=' '.join(myLabel.split('_')), w=150, align='left', p=self.tempLayout)
        mc.optionMenu('%sOptionMenu' % myLabel, l='', enable=False, w=80, p=self.tempLayout)
        for attr in attrs:
            mc.menuItem(attr)
        self.enumCheckBoxes.append(myLabel)

    def doubleCheckAttrEnumWidget(self, myLabel, flag, *attrs):
        myString = []
        for i, attr in enumerate(attrs):
            myString.append((i, attr))
        self.tempLayout = mc.rowLayout(nc=4, h=self.widgetHeight, p=self.flagLayout)
        myCheckBox = mc.checkBox('%sCheckBox' % myLabel, l='', w=20, ann=flag, cc=Callback(self.activateWidget, '%sAttrEnumIn' % myLabel, '%sAttrEnumOut' % myLabel), p=self.tempLayout)
        mc.text('%sText' % myLabel, l=' '.join(myLabel.split('_')), w=150, align='left', p=self.tempLayout)
        mc.attrEnumOptionMenu('%sAttrEnumIn' % myLabel, l='', ei=myString, enable=False, w=140, p=self.tempLayout)
        mc.attrEnumOptionMenu('%sAttrEnumOut' % myLabel, l='', ei=myString, enable=False, w=140, p=self.tempLayout)
        self.doubleEnumCheckBoxes.append(myLabel)

    def activateWidget(self, *args):
        for myWidget in args:
            wState = mc.control(myWidget, q=True, enable=True)
            mc.control(myWidget, e=True, enable=(1 - wState))
        
    def browse(self, widget, *args):
        myFolder = mc.fileDialog2(fileFilter='*.*', dialogStyle=2, fm=3)
        if myFolder:
            mc.textFieldButtonGrp(widget, e=True, fileName=myFolder[0])
            self.saveOptions()
        
    def saveOptions(self, *args):
        myValue = mc.textFieldButtonGrp(self.pathTextField, q=True, fileName=True)
        mc.optionVar(sv=['nMakeTx_makeTxPath', myValue])
        myValue = mc.radioButtonGrp(self.convertBehaviorRadioButton, q=True, sl=True)
        mc.optionVar(iv=['nMakeTx_convertOption', myValue - 1])
        
    def switchManage(self, widget, *args):
        currState = mc.control(widget, q=True, manage=True)
        mc.control(widget, e=True, manage=1 - currState)
        
    def convert(self, *args):
        
        # 0: 'Only not existing'
        # 1: 'Overwrite older'
        # 2: 'Overwrite all'
        
        # 0: from scene
        # 1: from folder
        
        flagString = ''
        lErrors = []
        
        # SIMPLE
        for myCheckBox in self.simpleCheckBoxes:
            if mc.checkBox('%sCheckBox' % myCheckBox, q=True, v=True):
                flagString += '%s ' % mc.checkBox('%sCheckBox' % myCheckBox, q=True, ann=True)
        # INT
        for myCheckBox in self.intCheckBoxes:
            if mc.checkBox('%sCheckBox' % myCheckBox, q=True, v=True):
                flagString += '%s %i ' % (mc.checkBox('%sCheckBox' % myCheckBox, q=True, ann=True), mc.intField('%sIntField' % myCheckBox, q=True, v=True))
                
         # DOUBLE INT
        for myCheckBox in self.doubleIntCheckBoxes:
            if mc.checkBox('%sCheckBox' % myCheckBox, q=True, v=True):
                flagString += '%s %i %i ' % (mc.checkBox('%sCheckBox' % myCheckBox, q=True, ann=True), mc.intField('%sIntFieldX' % myCheckBox, q=True, v=True), mc.intField('%sIntFieldY' % myCheckBox, q=True, v=True))
                
        # FLOAT
        for myCheckBox in self.floatCheckBoxes:
            if mc.checkBox('%sCheckBox' % myCheckBox, q=True, v=True):
                flagString += '%s %f ' % (mc.checkBox('%sCheckBox' % myCheckBox, q=True, ann=True), mc.floatField('%sFloatField' % myCheckBox, q=True, v=True))
                
        # ENUM
        # for myCheckBox in self.enumCheckBoxes:
            # if mc.checkBox('%sCheckBox' % myCheckBox, q=True, v=True):
                # flagString += '%s %s ' % (mc.checkBox('%sCheckBox' % myCheckBox, q=True, ann=True), mc.attrEnumOptionMenu('%sOptionMenu' % myCheckBox, q=True))
         
        # OPTION MENU
        for myCheckBox in self.enumCheckBoxes:
            if mc.checkBox('%sCheckBox' % myCheckBox, q=True, v=True):
                flagString += '%s %s ' % (mc.checkBox('%sCheckBox' % myCheckBox, q=True, ann=True), mc.optionMenu('%sOptionMenu' % myCheckBox, q=True, v=True))

        makeTxPath = mc.textFieldButtonGrp(self.pathTextField, q=True, fileName=True)
        convertType = mc.radioButtonGrp(self.convertBehaviorRadioButton, q=True, sl=True) - 1
        sourceType = mc.radioButtonGrp(self.textureFrom, q=True, sl=True) - 1
        showTerminal = mc.checkBox('verboseCheckBox', q=True, v=True)
        
        if not os.path.isfile('%s/maketx.exe' % makeTxPath):
            MGlobal.displayInfo('[ERROR] Unable to find makeTx.exe. Exit!')
            return
            
        if not len(mc.ls(type='file')) and not sourceType:
            MGlobal.displayInfo('[WARNING] No textures in current scene. Nothing to convert.')
            return
        
        myFileList = []
        if sourceType:
            myTextureFolder = mc.textFieldButtonGrp(self.texturePathTextField, q=True, fileName=True)
            imageFormats = [  '.bmp', '.cin', '.dds', '.dpx', '.f3d', '.fits', '.hdr', '.hdri', '.ico', '.iff', '.jpg', '.jpeg',
                                        '.jif', '.jfif', '.jfi', '.jp2', '.j2k', '.exr', '.png', '.pbm', '.pgm', '.ppm', '.ptex', '.rla',
                                        '.sgi', '.rgb', '.rgba', '.pic', '.tga', '.tif', '.tiff'  ]
                            
            for (fileFolder, folders, files) in os.walk(myTextureFolder):
                for file in files:
                    if os.path.splitext(file)[-1] in imageFormats:
                        myFileList.append(os.path.join(fileFolder, file))

        else:
            for fileNode in mc.ls(type='file'):
                myFileList.append(mc.getAttr('%s.fileTextureName' % fileNode))

        #Setting up the progress bar.
        x = len(myFileList)
        counter = 0
        mc.progressBar(self.progressControl, e=True, maxValue=x)

        mc.columnLayout(self.progressLayout, e=True, manage=True)
        mc.refresh(f=True)
        
        for i, texFileIn in enumerate(myFileList):

            myPath, myFile = os.path.split(texFileIn)
            myFile, myExt = os.path.splitext(myFile)
            texFileOut = '%s/%s.tx' % (myPath, myFile)

            progressInc = mc.progressBar(self.progressControl, edit=True, pr=counter)
            mc.text(self.currentNumberText, e=True, l='Processing file %i / %i' % (i+1, x))
            mc.text(self.currentFileText, e=True, l='%s%s' % (myFile, myExt))
            mc.refresh(f=True)
            
            if not os.path.isfile(texFileOut) or convertType == 2:
                MGlobal.displayInfo('[INFO] %s --> %s' % (texFileIn, texFileOut))
                call('%s/maketx.exe %s "%s"' % (makeTxPath, flagString, texFileIn), shell=1 - showTerminal)
                # Check if the texture has been converted and add the errors to a list
                if not os.path.isfile(texFileOut):
                        lErrors.append(texFileOut)
                
            elif convertType == 1:
                sourceFileDate = datetime.datetime.fromtimestamp(os.path.getmtime(texFileIn))
                
                try:
                    with open(texFileOut, 'r') as f:
                        destFileDate = datetime.datetime.fromtimestamp(os.path.getmtime(texFileOut))
                except:
                    destFileDate = datetime.datetime.min
                
                if sourceFileDate > destFileDate:
                    MGlobal.displayInfo('[INFO] %s updated' % (texFileOut))
                    call('%s/maketx.exe %s "%s"' % (makeTxPath, flagString, texFileIn), shell=1 - showTerminal)
                    
                    # Check if the texture has been converted and add the errors to a list
                    if not os.path.isfile(texFileOut):
                        lErrors.append(texFileOut)
            
                else:
                    MGlobal.displayInfo('[INFO] %s is up to date' % (texFileOut))
                    
            else:
                MGlobal.displayInfo('[INFO] %s already present, skipped' % texFileOut)
            
            counter = counter + 1 
            
        mc.columnLayout(self.progressLayout, e=True, manage=False)
        
        if lErrors:
            MGlobal.displayInfo('[ERROR] unable to write the following files: %s' % lErrors)

# Class used to pass arguments to commands (like with buttons)
class Callback(object): 
        def __init__(self, func, *args, **kwargs): 
                self.func = func 
                self.args = args 
                self.kwargs = kwargs
        def __call__(self, *args): 
                return self.func( *self.args, **self.kwargs )