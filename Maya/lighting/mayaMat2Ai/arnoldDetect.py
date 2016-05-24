import maya.cmds as cmds

def arnoldDetect():

    if cmds.pluginInfo('mtoa.mll', query=True, l=True):
        print "Arnold already loaded"
        return True
    else:
        cmds.loadPlugin('mtoa.mll', quiet=True)
        print "Loading Arnold"
        return True
