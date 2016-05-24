import maya.cmds as cmds


def convertTexPath():

    sl = cmds.ls(selection=1)

    non_tex_count = 0

    for i in sl:
        try:
            path = cmds.getAttr(i + ".fileTextureName").split("/")
            subFolder = path[-2]
            fileName = path[-1]

            #print subFolder,",", fileName

            if path is not None or path != "":
                cmds.setAttr(i + ".fileTextureName",
                             "%s/%s" % (subFolder, fileName), type="string")
        except:
            non_tex_count += 1
        else:
            pass

    print "there is %d non texture node" % non_tex_count
