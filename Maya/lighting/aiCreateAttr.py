# 256 pipeline tools
# add attributes mtoa_constant_ of different data types to an jbject shapes
# select jject shapes, run script
# possible enter several attribute names with spase(mMask_A mMask_B mMask_C)
# Put script to \Documents\maya\201X-x64\scripts
# In Python tab of Maya script editor execute code:
# import aiCreateAttr
# aiCreateAttr.windowADD()


import pymel.core as pm
import random as rand
from functools import partial

def randCol():
    c1 = rand.uniform(0,1)
    c2 = rand.uniform(0,1)
    c3 = rand.uniform(0,1)
    return (c1,c2,c3)

def genMat(*args):
    selected = pm.ls(sl=1,long=1)

    matName= 'master_attr_mat'
    existAttrMat = pm.ls((matName),materials=True)
    masterMat = False

    if (len(existAttrMat) ==0):
        rn1 = rand.uniform(0,1)
        rn2 = rand.uniform(0,1)
        rn3 = rand.uniform(0,1)
        # create master material andol 5
        masterMat = pm.shadingNode( 'aiStandardSurface',name=matName, asShader=True )
        pm.setAttr ( (masterMat + '.baseColor'), randCol(), type = 'double3' )

        #create vrtx col hook and boolean
        diffVrtx = pm.shadingNode('aiUserDataColor', name='diffVrtxAttr',asTexture=True)
        pm.setAttr ((diffVrtx + '.colorAttrName'), 'colorSet1', type = 'string')
        pm.setAttr ((diffVrtx + '.defaultValue'), (rand.uniform(0,1)),(rand.uniform(0,1)),(rand.uniform(0,1)), type = 'double3')
        # create diff col attr
        diffCol = pm.shadingNode('aiUserDataColor', name='diffColAttr',asTexture=True)
        pm.setAttr ((diffCol + '.colorAttrName'), 'diffCol', type = 'string')
        pm.setAttr ((diffCol + '.defaultValue'), (rand.uniform(0,1)),(rand.uniform(0,1)),(rand.uniform(0,1)), type = 'double3')
        # bool attribute for vrtx diff
        diffVrtxBool = pm.shadingNode('aiUserDataBool', name='diffVrtxBool',asUtility=True)
        pm.setAttr ((diffVrtxBool + '.boolAttrName'), 'diffVrtxTog', type = 'string')
        pm.setAttr ((diffVrtxBool + '.defaultValue'), False)
        # switch between diff col and dif vrtx
        diffColSwitch = pm.shadingNode('colorCondition', name='useDiffVrtx',asUtility=True)
        pm.connectAttr((diffVrtx +'.outColor'), (diffColSwitch +'.colorA'))
        pm.connectAttr((diffVrtx +'.outTransparencyR'), (diffColSwitch +'.alphaA'))
        pm.connectAttr((diffCol +'.outColor'), (diffColSwitch +'.colorB'))
        pm.connectAttr((diffCol +'.outTransparencyR'), (diffColSwitch +'.alphaB'))
        pm.connectAttr((diffVrtxBool +'.outValue'), (diffColSwitch +'.condition'))

        #create difftex attribute and empty texture file
        diffTexStr = pm.shadingNode('aiUserDataString', name='diffTexAttr',asUtility=True)
        pm.setAttr ((diffTexStr + '.stringAttrName'), 'diffTex', type = 'string')
        diffTexFile = pm.shadingNode('file', name='diffTexFile',asTexture=True)
        pm.connectAttr((diffTexStr +'.outValue'), (diffTexFile +'.fileTextureName'))
        # bool and switch attribute after vrtx col vs attr col to diff tex
        diffTexBool = pm.shadingNode('aiUserDataBool', name='diffTexBool',asUtility=True)
        pm.setAttr ((diffTexBool + '.boolAttrName'), 'diffTexTog', type = 'string')
        pm.setAttr ((diffTexBool + '.defaultValue'), False)
        # switch between diff atr branch and dif file
        diffTexSwitch = pm.shadingNode('colorCondition', name='useDiffTex',asUtility=True)
        pm.connectAttr((diffTexFile +'.outColor'), (diffTexSwitch +'.colorA'))
        pm.connectAttr((diffTexFile +'.outAlpha'), (diffTexSwitch +'.alphaA'))
        pm.connectAttr((diffColSwitch +'.outColor'), (diffTexSwitch +'.colorB'))
        pm.connectAttr((diffColSwitch +'.outAlpha'), (diffTexSwitch +'.alphaB'))
        pm.connectAttr((diffTexBool +'.outValue'), (diffTexSwitch +'.condition'))


        pm.connectAttr((diffTexSwitch +'.outColor'), (masterMat +'.baseColor'))
        pm.connectAttr((diffTexSwitch +'.outAlpha'), (masterMat +'.opacityR'))
        pm.connectAttr((diffTexSwitch +'.outAlpha'), (masterMat +'.opacityG'))
        pm.connectAttr((diffTexSwitch +'.outAlpha'), (masterMat +'.opacityB'))

        #masterMatShadingGroup=pm.shadingNode('shadingEngine',name=(masterMat + '_SG'),asShader=True)
        #pm.connectAttr((masterMat +'.outColor'), (masterMatShadingGroup +'.surfaceShader'))
    else:
        masterMat = existAttrMat[0]
    for member in selected:
    	pm.select(member)
        pm.hyperShade(member,assign=masterMat )

    pm.select(selected)
#genMat()


def connectMat(*args):
    pass

def addFloatAttr(*args):
    floatAttrName = pm.textFieldGrp( 'floatText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                pm.addAttr(member, ln = "mtoa_constant_" + i, nn = i,hasMaxValue=False,hasMinValue=False, dv =1.0,smn=0, smx=9)

def delFloatAttr(*args):
    floatAttrName = pm.textFieldGrp( 'floatText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                pm.deleteAttr(member + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'

def addStringAttr(*args):
    stringAttrName = pm.textFieldGrp( 'stringText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in stringAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                pm.addAttr(member, ln = "mtoa_constant_" + i, nn = i, dt = 'string')
def delStringAttr(*args):
    floatAttrName = pm.textFieldGrp( 'stringText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                pm.deleteAttr(member + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'

def addColorAttr(*args):
    colorAttrName = pm.textFieldGrp( 'colorText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in colorAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                pm.addAttr(member, ln = "mtoa_constant_" + i, nn = i , uac = 1, at ="float3" )
                pm.addAttr(member, ln = "red_" + i, at = "float", p = "mtoa_constant_" + i )
                pm.addAttr(member, ln = "grn_" + i, at = "float", p = "mtoa_constant_" + i )
                pm.addAttr(member, ln = "blu_" + i, at = "float", p = "mtoa_constant_" + i )
                pm.setAttr(member +".mtoa_constant_" + i, randCol())
                randCol

def delColorAttr(*args):
    floatAttrName = pm.textFieldGrp( 'colorText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                pm.deleteAttr(member + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'

def addIntAttr(*args):
    stringAttrName = pm.textFieldGrp( 'intText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in stringAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                pm.addAttr(member, ln = "mtoa_constant_" + i, nn = i, at = 'long')

def delIntAttr(*args):
    floatAttrName = pm.textFieldGrp( 'intText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                pm.deleteAttr(member + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'

def addBoolAttr(*args):
    stringAttrName = pm.textFieldGrp( 'boolText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in stringAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                print 'attribute ' + i + ' already exist!'
            else:
                pm.addAttr(member, ln = "mtoa_constant_" + i, nn = i, at = 'bool')

def delBoolAttr(*args):
    floatAttrName = pm.textFieldGrp( 'boolText', q = True, text = True ).split(' ')
    pm.pickWalk( d = "down" )
    selected = pm.ls(sl=1,long=1)
    for member in selected:
        for i in floatAttrName:
            if pm.attributeQuery( "mtoa_constant_" + i, node = member, exists = True ):
                pm.deleteAttr(member + '.mtoa_constant_' + i)
            else:
                print 'attribute ' + i + ' not exist!'

def addAll(*agrs):
    addStringAttr()
    addBoolAttr()
    addColorAttr()
    addFloatAttr()

def delAll(*args):
    delFloatAttr()
    delStringAttr()
    delColorAttr()
    delBoolAttr()

def windowADD(*args):
    tw = 250
    cw = 50
    fw = 350
    hw = fw /2
    fh = 50

    if pm.window("myWin", exists = 1):
        pm.deleteUI("myWin")
    win = pm.window("myWin", title = "ADD ATTRIBUTES", w = fw, h = 100, sizeable = 0)

    mainLayout = pm.columnLayout(w=fw)
    startLayout = pm.rowColumnLayout(cw=((1,tw),(2,cw),(3,cw)),nc = 3,
                                    cal=((1,'left'),(2,'left'),(3,'left')),
                                    co=((1,'left',1),(2,'left',1),(3,'left',1)),
                                    parent=mainLayout)

    pm.textFieldGrp( 'stringText', w = tw, text = 'diffTex dispTex emissT sssTex',parent=startLayout)
    pm.button (label = "ADD S", w = cw, c = addStringAttr)
    pm.button (label = "DEL S", w = cw, c = delStringAttr)
    pm.textFieldGrp( 'boolText', w = tw, text = 'diffTexTog diffVrtxTog')
    pm.button (label = "ADD B", w = cw, c = addBoolAttr)
    pm.button (label = "DEL B", w = cw, c = delBoolAttr)
    pm.textFieldGrp( 'colorText', w = tw, text = 'diffCol specCol emissCol rougCol sssCol')
    pm.button (label = "ADD C", w = cw, c = addStringAttr)
    pm.button (label = "DEL C", w = cw, c = delStringAttr)
    pm.textFieldGrp( 'floatText' , w = tw, text = 'bumpVal specVal iorVal rougVal reflVal refrVal emisVal')
    pm.button (label = "ADD F", w = cw, c = addFloatAttr)
    pm.button (label = "DEL F", w = cw, c = delFloatAttr)
    pm.textFieldGrp( 'intText' , w = tw, text = 'lightGroup istanceID')
    pm.button (label = "ADD I", w = cw, c = addIntAttr)
    pm.button (label = "DEL I", w = cw, c = delIntAttr)

    midLayout = pm.rowColumnLayout(cw=((1,hw),(2,hw)),co=((1,'left',1),(2,'left',1)), nc = 2,parent=mainLayout)

    pm.button (label = 'ADD ALL', w= hw, h = fh,parent=midLayout, c = addAll)
    pm.button (label = 'DELETE ALL', w= hw, h = fh,parent=midLayout, c = delAll)

    pm.button (label = 'MASTER MATERIAL', w= fw, h = fh,parent=mainLayout, c = genMat)

    pm.showWindow(win)
#windowADD()
