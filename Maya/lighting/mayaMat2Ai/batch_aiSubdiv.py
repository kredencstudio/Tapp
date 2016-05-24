import maya.cmds as cmds

"""

Batch Change aiSubDiv Type

Useage:

batch_aiSubDiv("catclark")
batch("catclark")

Arguments:

"catclark", "linear", "none"

"""

def batch_aiSubdiv(subdivType="catclark"):

    attName = "aiSubdivType"
    subdivTypeKey = {"catclark":1, "linear":2, "none":0}

    setTypeTo = subdivTypeKey[subdivType]

    sl = cmds.ls(selection=1)

    for i in sl:
        # Get Shapes
        if cmds.ls(i, transforms=1):
            shapes = cmds.listRelatives(i, fullPath=1, children=1, shapes=1)
            shape = shapes[0]   
        else: 
            shape = i     
            
        try:
            cmds.setAttr("%s.%s"%(shape,attName), setTypeTo)
        except:
            print "non Arnold Geo"
        else:
            pass

def batch(subdivType="catclark"):
    batch_aiSubdiv(subdivType)
