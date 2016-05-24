import maya.cmds as cmds
import pymel.core as pm


import mtoa.core as core

def loadArnold():
    cmds.loadPlugin('mtoa.mll', quiet=True)
    cmds.setAttr('defaultRenderGlobals.ren', 'arnold', type='string')
    print 'Arnold renderer loaded'


def aiSetSubd(aiSubdType):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(selection=True, dag=True, lf=True, type='mesh')
    for i in sel:
        cmds.setAttr( i + '.aiSubdivType', aiSubdType)

def aiSetIter(iterValue):
    cmds.pickWalk( d = "down" )
    sel = cmds.ls(selection=True, dag=True, lf=True, type='mesh')
    for i in sel:
        cmds.setAttr( i + '.aiSubdivIterations', iterValue)


def MaskBuild():

    # sel = cmds.ls(selection=True)

    sets = cmds.ls(sets=True)

    aiMaskSets = []
    for node in sets:
        if node.startswith('aiMask'):
            aiMaskSets.append(node)

    maskDic = {}
    for s in aiMaskSets:
        # find layers
        if ('aiMask' in s) and (('_') not in s):
            maskDic[s] = {}

    for layer in maskDic:
        for s in aiMaskSets:
            if s.startswith(layer + "_"):
                channel = s.split('_')[1]
                print pm.PyNode(s).members()
                maskDic[layer][channel] = pm.PyNode(s).members()

    print maskDic

    if not aiMaskSets:
        cmds.warning('No sets selected!')
        return

    core.createOptions()

    for layer in maskDic:
        aiColor = addIdShader(layer)
        print maskDic[layer]
        for channel in maskDic[layer]:
            for shape in maskDic[layer][channel]:
                # pm_shape = pm.PyNode(shape)
                attr = addColor(shape, layer, channel)

        addAOV(layer, aiColor)

def addIdShader(layer):

    aiColorName = layer + '_aiUserDataColor'

    try:
        aiColor = pm.PyNode(aiColorName)
        print "aiColor Exists"
    except pm.MayaObjectError:
        aiColor = cmds.shadingNode('aiUserDataColor', asShader=1, n=aiColorName)
        cmds.setAttr(aiColor + '.colorAttrName', layer, typ='string')
        print "aiColor was created"



    return aiColor

def addAOV(layer, aiColor):
    # AOV
    aovListSize = cmds.getAttr('defaultArnoldRenderOptions.aovList', s=1)

    aov_name = 'aiAOV_' + layer

    if cmds.objExists(aov_name):
        customAOV = aov_name
        print "AOV Exists"
    else:
        customAOV = cmds.createNode('aiAOV',
                                    n=aov_name,
                                    skipSelect=True)
        cmds.setAttr(customAOV + '.name', layer,
                     type='string')
        cmds.connectAttr(customAOV + '.message',
                         'defaultArnoldRenderOptions.aovList[' + str(aovListSize) + ']',
                         f=1)

        cmds.connectAttr('defaultArnoldDriver.message',
                         customAOV + '.outputs[0].driver', f=1)
        cmds.connectAttr('defaultArnoldFilter.message',
                         customAOV + '.outputs[0].filter', f=1)

        # connect to default shader
        cmds.connectAttr(aiColor + '.outColor',
                         customAOV + '.defaultValue', f=1)
        print "AOV was created"

    return customAOV


def addColor(node, layer, color): #create color attribute

    colorAttrName = layer
    colorAttrNameLong = 'mtoa_constant_' + colorAttrName

    if node.hasAttr(colorAttrNameLong):
        node.deleteAttr(colorAttrNameLong)

    node.addAttr(colorAttrNameLong, niceName=colorAttrName, usedAsColor=True, attributeType='float3')
    node.addAttr('R' + str(colorAttrName), attributeType='float', parent=colorAttrNameLong)
    node.addAttr('G' + str(colorAttrName), attributeType='float', parent=colorAttrNameLong)
    node.addAttr('B' + str(colorAttrName), attributeType='float', parent=colorAttrNameLong)

    colors = {
        'red': [(1, 0, 0), 13],
        'green': [(0, 1, 0), 14],
        'blue': [(0, 0, 1), 6]
        }
    node.setAttr(colorAttrNameLong, colors[color][0])

    node.overrideEnabled.set(True)
    node.overrideColor.set(colors[color][1])

    return colorAttrNameLong


def setIdColor(color, layerNum):
    sel = pm.ls(sl=True)

    layerName = 'aiMask' + str(layerNum)
    colorLayerName = '{}*{}'.format(layerName, color)

    layerNodes = pm.ls('*aiMask*')
    layerSets = pm.ls(layerNodes, sets=True)
    layerAOV = pm.ls(layerNodes, typ='aiAOV')
    layerShader = pm.ls(layerNodes, typ='aiUserDataColor')

    shapes = []
    for s in sel:
        try:
            s = s.getShape()
        except:
            pass
        shapes.append(s)

    if not pm.objExists(layerName):
        makeIdSets(layerNum)

    if not pm.objExists(colorLayerName):
        cmds.warning("Missing id set for chosen color and layer. Remove the whole layer set or create the appropriate color set")
        return

    colorSet = pm.ls(colorLayerName, sets=True)[0]

    for s in shapes:

        for l in layerSets:
            try:
                l.remove(s)
            except:
                pass

        colorSet.add(s)
        colorSet.forceElement(s)

        addColor(s, layerName, color)

    aiColor = addIdShader(layerName)
    addAOV(layerName, aiColor)


def checkMaskLayers(*args):#check existing ids to create proper nubers for next ids
    objsets = pm.ls('*aiMask*', sets=True)
    layers = []
    for set in objsets:
        if '_' not in set.name():
            layers.append(set)

    i = len(layers) + 1

    return i

def makeIdSets(i=None):

    if not i:
        i = checkMaskLayers()

    sel = pm.ls(sl=True)
    pm.select(clear=True)

    name = 'aiMask' + str(i)

    rSet = pm.sets(n=name + '_red')
    gSet = pm.sets(n=name + '_green')
    bSet = pm.sets(n=name + '_blue')

    pm.sets(rSet, gSet, bSet, n=name)

    pm.select(sel)

    return rSet, gSet, bSet

def MaskFlush():

    aovs = cmds.ls(type='aiAOV')
    nodes = []
    for aov in aovs:
        if 'aiMask' in aov:
            nodes.append(aov)
            ut = cmds.listConnections(aov, type='aiUserDataColor')
            if ut:
                nodes.extend(ut)
    if nodes:
        cmds.delete(nodes)

def clearIDs():

    sel = pm.ls(sl=True)

    for node in sel:
        try:
            node = node.getShape()
        except:
           pass
        attrs = node.listAttr(ud=True, m=True)
        for attr in attrs:
            if 'mtoa_constant_aiMask' in attr.name():
                print attr
                attr.delete()
        node.overrideEnabled.set(False)
        node.overrideColor.set(5)


def addAOVlightGroup(lightGroup):
    # AOV
    aovListSize = cmds.getAttr('defaultArnoldRenderOptions.aovList', s=1)

    name = 'light_group_' + lightGroup
    aov_name = 'aiAOV_light_group_' + name

    if cmds.objExists(aov_name):
        customAOV = aov_name
        print "AOV Exists"
    else:
        customAOV = cmds.createNode('aiAOV',
                                    n=aov_name,
                                    skipSelect=True)
        cmds.setAttr(customAOV + '.name', name,
                     type='string')

        cmds.connectAttr(customAOV + '.message',
                         'defaultArnoldRenderOptions.aovList[' + str(aovListSize) + ']',
                         f=1)

        cmds.connectAttr('defaultArnoldDriver.message',
                         customAOV + '.outputs[0].driver', f=1)
        cmds.connectAttr('defaultArnoldFilter.message',
                         customAOV + '.outputs[0].filter', f=1)

        print "AOV was created"

    return customAOV


def addToLightGroup(lightGroup):
    name = 'lightGroup'
    attrName = 'mtoa_constant_' + name
    cmds.pickWalk(d="down")
    selected = cmds.ls(sl=1, long=1)

    addAOVlightGroup(lightGroup)

    for member in selected:
        if cmds.attributeQuery(attrName, node=member, exists=True):
            print 'attribute ' + attrName + ' already exist!'
        else:
            cmds.addAttr(member, ln=attrName, nn=name, at='long')

        cmds.setAttr(member + '.' + attrName, int(lightGroup))



def Mask():

    MaskFlush()
    MaskBuild()
