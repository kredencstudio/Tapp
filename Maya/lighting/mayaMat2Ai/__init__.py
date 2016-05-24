import maya.cmds as cmds
import maya.mel as mel

import mayaMat2Ai
reload(mayaMat2Ai)

from arnoldDetect import arnoldDetect

from convertTexPath2RealtivePath import convertTexPath

from batch_aiSubdiv import batch_aiSubdiv

##
## Package Function
##


def convert(type='aiStandard', proxy=False):

    sl = cmds.ls(selection=1)

    if len(sl) == 0:
        print "nothing selected!"

    # try:
    #     cmds.loadPlugin('mtoa.mll', quiet=True)
    # except:
    #     print

    mats=set()
    for node in sl:
        nodeType = cmds.ls(node, showType=1)[1]
        if nodeType in ['transform', 'mesh']:
            shape = cmds.ls(node, s=1, dag=1)
            SgNodes = cmds.listConnections(shape, type='shadingEngine')
            matMaya = cmds.listConnections(SgNodes[0] + '.surfaceShader')[0]
        else:
            matMaya = node

    mats.add(matMaya)
    print mats

    if cmds.pluginInfo('mtoa.mll', query=True, l=True):
        print "Arnold already loaded"
    else:
        cmds.loadPlugin('mtoa.mll', quiet=True)
        print "Loading Arnold"
    # if arnoldDetect():
    #     pass
    # else:
    #     print 'OOps'
    #     return None

    non_convert = 0
    non_convert_List = []

    mM2Ai = mayaMat2Ai.mayaMat2Ai()

    for i in mats:
        print i

        if i == "lambert1":       # skip the default lambert shader
            print "Cannot convert default lambert shader"
            continue

        mType = cmds.ls(i, showType=1)[1]

        if mM2Ai.matchM(mType):

            mM2Ai.defaultType = type
            mM2Ai.leave_proxy = proxy

            if mM2Ai.convert(mType, i):
                print "ok!"

            else:
                non_convert_List.append(i)
                non_convert += 1
                print "%s: convert op failed!" % i

        else:
            non_convert_List.append(i)
            non_convert += 1
            print "%s: no material match type!" % i

    if len(non_convert_List) > 0:
        print "list of material not converted:"
        for i in non_convert_List:

            print i

    print "%d material fail to convert" % non_convert


def trimTexPath():
    convertTexPath()

def batch(subdivType="catclark"):
    batch_aiSubdiv(subdivType)

def test():

    sl = cmds.ls(selection=1)
    mM2Ai = mayaMat2Ai.mayaMat2Ai()

    print mM2Ai.getConnected(sl[0])
