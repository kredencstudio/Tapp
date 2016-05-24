import maya.cmds as cmds
import maya.mel as mel


class mayaMat2Ai():

    matList = ["phong", "blinn", "lambert"]
    convertType = None
    aiName = "aiStandard_"
    leave_proxy = False

    # Maya Attr Name

    getAttrList = [".color",
                   ".specularColor", ".cosinePower",
                   ".specularRollOff", ".eccentricity",
                   ".ambientColor", ".incandescence", ".diffuse"]

    downAttList = [".outColor"]
    upAttList = [".color", ".ambientColor", ".incandescence", ".normalCamera"]

    # aiStandard Attr Name

    aiDiffColor = ".color"  # type double3
    aiDiffWeight = ".Kd"
    aiDiffRoughness = "diffuseRoughtness"

    aiSpecColor = ".KsColor"  # type double3
    aiSpecWeight = ".Ks"
    aiSpecRoughness = ".specularRoughness"
    aiSpecFresnel = ".specularFresnel"
    aiFresnel_Coe = ".Ksn"

    aiBump = ".normalCamera"

    aiEmissionColor = ".emissionColor"
    aiEmissionScale = ".emission"

    aiTransparencyList = [".Kt", ".opacity"]

    useaiTransparency = False       # By Default Don't Use Tranparency slot

    createdNodeList = []

    # defaultType = "aiStandard"
    defaultType = "alSurface"

    verbose = True

    def __init__(self):

        if self.verbose:
            print "list of current defined material type is"
            print self.matList

    def matchM(self, mType):

        verbose = self.verbose

        if verbose:
            print "incoming type is %s" % mType

        for mat in self.matList:

            if mType == mat:
                self.convertType = mType
                match = True
                break
            else:
                match = False

        return match

    def convert(self, type, mayaMat):

        self.prepare_attributes()

        if type == "phong":
            result = self.phong2Ai(mayaMat)

        if type == "blinn":
            result = self.blinn2Ai(mayaMat)

        if type == "lambert":
            result = self.lambert2Ai(mayaMat)

        return result

    def lambert2Ai(self, mayaMat):

        if mayaMat:

            connectDict = self.getConnected(node=mayaMat)
            print connectDict
            attrList = self.getAttrs(node=mayaMat)

            newNode = self.createAiShadingNode(nodeName=mayaMat,
                                               createType=self.defaultType)

            cmds.select(clear=1)

            self.createdNodeList.append(newNode)

            self.connect_alpha(newNode, mayaMat)

            self.setShadingAttrs(newNode, attrList)

            # mel.eval("replaceNode \"%s\" \"%s\";" % (mayaMat, newNode))
            self.reconnectShadingNetwork2(newNode, mayaMat, connectDict)

            self.convertEmission(attrList, newNode)

            cmds.setAttr(newNode + self.aiSpecWeight, 0)
            if not self.leave_proxy:
                cmds.delete(mayaMat)

            return True

        else:
            return False

    def phong2Ai(self, mayaMat):

        if mayaMat:

            connectDict = self.getConnected(node=mayaMat)
            attrList = self.getAttrs(node=mayaMat)

            newNode = self.createAiShadingNode(nodeName=mayaMat,
                                               createType=self.defaultType)

            cmds.select(clear=1)

            self.createdNodeList.append(newNode)

            self.connect_alpha(newNode, mayaMat)

            # mel.eval("replaceNode \"%s\" \"%s\";" % (mayaMat, newNode))
            self.reconnectShadingNetwork2(newNode, mayaMat, connectDict)


            cmds.setAttr(newNode + SpecWeight, 1)
            cmds.setAttr(newNode + SpecFresnel, 1)

            for attr in attrList:

                if attr[0] == ".specularColor":
                    cmds.setAttr(newNode + specColor,
                                 attr[1][0][0], attr[1][0][1], attr[1][0][2],
                                 type="double3")

                if attr[0] == ".cosinePower":
                    if attr[1] > 0:
                        cmds.setAttr(newNode + SpecRoughness,
                                     1 / attr[1])

            self.convertEmission(attrList, newNode)

            return True

        else:
            return False

    def blinn2Ai(self, mayaMat):

        if mayaMat:

            connectDict = self.getConnected(node=mayaMat)
            print connectDict
            attrList = self.getAttrs(node=mayaMat)

            newNode = self.createAiShadingNode(nodeName=mayaMat,
                                               createType=self.defaultType)

            cmds.select(clear=1)

            self.createdNodeList.append(newNode)

            self.connect_alpha(newNode, mayaMat)

            # try:
            #     mel.eval("replaceNode \"%s\" \"%s\";" % (mayaMat, newNode))
            # except:
            self.reconnectShadingNetwork2(newNode, mayaMat, connectDict)

            cmds.setAttr(newNode + self.aiSpecWeight, 1)
            cmds.setAttr(newNode + self.aiSpecFresnel, 1)

            for attr in attrList:

                if attr[0] == ".specularColor":
                    cmds.setAttr(newNode + self.aiSpecColor,
                                 attr[1][0][0], attr[1][0][1], attr[1][0][2],
                                 type="double3")

                if attr[0] == ".ambientColor":
                    cmds.setAttr(newNode + self.aiEmissionColor,
                                 attr[1][0][0], attr[1][0][1], attr[1][0][2],
                                 type="double3")

                if attr[0] == ".eccentricity":
                    cmds.setAttr(newNode + self.aiSpecRoughness, attr[1])

            self.convertEmission(attrList, newNode)

            return True

        else:
            return False

    def connect_alpha(self, newNode, mayaMat):

        alpha_attr1 = '.transparency'
        alpha_attr2 = '.matteOpacity'  # may use this in the future

        if cmds.connectionInfo(mayaMat + "%s" % alpha_attr1, isDestination=1):
            plug_source = cmds.connectionInfo(mayaMat + "%s" % alpha_attr1,
                                              sourceFromDestination=1)

            node_source = plug_source.split(".")[0]

            node_outAlpha = node_source + '.outAlpha'
            node_outTransparency = node_source + '.outTransparency'

            for i in self.aiTransparencyList:
                if ".opacity" in i:
                    print 'opacity mode'
                    try:
                        cmds.connectAttr(node_outTransparency, newNode + i)
                    except:
                        cmds.connectAttr(node_outAlpha, newNode + i)

                if i == ".Kt" and self.useaiTransparency is True:
                    cmds.connectAttr(node_outTransparency, newNode + i)

            print "alpha connect ok!"
            return True

        else:
            return False

    def convertEmission(self, attrList, newNode):

        for attr in attrList:

            if attr[0] == ".ambientColor":
                cmds.setAttr(newNode + self.aiEmissionColor,
                             attr[1][0][0], attr[1][0][1], attr[1][0][2],
                             type="double3")
                cmds.setAttr(newNode + self.aiEmissionScale, 1)

            if attr[0] == ".incandescence":
                if attr[1][0] > (0, 0, 0):
                    cmds.setAttr(newNode + self.aiEmissionColor,
                                 attr[1][0][0], attr[1][0][1], attr[1][0][2],
                                 type="double3")
                    cmds.setAttr(newNode + self.aiEmissionScale, 1)

    def reconnectShadingNetwork2(self, newNode, mayaMat, connectDict):

        connectList = connectDict["all"]
        up = connectDict["up"]
        down = connectDict["down"]
        source = connectDict["source"]
        destination = connectDict["destination"]

        print source
        print destination

        for pair in destination:
            print pair[0]
            source_plug = pair[0]
            for plug in pair[1]:
                print plug
                attr = plug.split(".")[-1]
                try:
                    if attr == 'color':
                        cmds.connectAttr(source_plug, newNode + self.aiDiffColor)
                    else:
                        cmds.connectAttr(source_plug, newNode + "." + attr)
                except:
                    print 'Could not connect {} to {}'.format(source_plug, (newNode + "." + attr))

        for pair in source:
            source_plug = pair[0]
            dest_plug = pair[1]
            # if cmds.connectionInfo(plug, isSource=1):
            #     dest_plug = cmds.connectionInfo(plug, destinationFromSource=1)
            attr = source_plug.split(".")[-1]
            print newNode + "." + attr
            try:
                if attr == 'outColor':
                    if self.leave_proxy:
                        dest_plug = dest_plug.split(".")[0] + '.aiSurfaceShader'
                print dest_plug
                cmds.connectAttr(newNode + "." + attr, dest_plug, force=True)

            except:
                print 'Could not connect {} to {}'.format((newNode + "." + attr), dest_plug)

    def setShadingAttrs(self, newNode, attrList):

        for attr in attrList:
            print attr
            if attr[0] == '.color':
                cmds.setAttr(newNode + self.aiDiffColor, attr[1][0][0], attr[1][0][1], attr[1][0][2],
                type="double3")
            if attr[0] == '.diffuse':
                cmds.setAttr(newNode + self.aiDiffWeight, attr[1])

    def createAiShadingNode(self, nodeName="", createType="aiStandard"):

        if nodeName and createType:
            cmds.shadingNode(createType, asShader=True)

            current = cmds.ls(selection=1)[0]

            newName = current + "_" + nodeName

            cmds.rename(current, newName)

            return newName
        else:
            print "Node name or type not valid, %s is not created" % createType
            return False

    def getAttrs(self, node=None):

        if node:
            pass
        else:
            return False

        attrList = []

        for attr in self.getAttrList:
            try:
                attrList.append([attr, cmds.getAttr(node + attr)])
            except:
                pass
            else:
                pass

        return attrList

    def getConnected(self, node=None):

        if node:
            pass
        else:
            return False

        connectList = []
        upList = []
        downList = []

        sourceList = []
        destList = []

        connections = cmds.listConnections(node, p=True)

        print connections

        if connections:

            for plug in connections:

                if cmds.connectionInfo(plug, isDestination=1):

                    connectList.append(plug)
                    upList.append(plug)

                if cmds.connectionInfo(plug, isSource=1):

                    connectList.append(plug)
                    downList.append(plug)

            for plug in upList:
                source_plug = cmds.connectionInfo(plug,
                                                  sourceFromDestination=1)

                sourceList.append([source_plug, plug])

            for plug in downList:
                dest_plug = cmds.connectionInfo(plug,
                                                destinationFromSource=1)

                destList.append([plug, dest_plug])

        connectDict = {"up": upList, "down": downList,
                       "source": sourceList, "destination": destList,
                       "all": connectList}

        return connectDict

    def prepare_attributes(self):

        if self.defaultType == 'alSurface':
            # alSurface Attr Name

            self.aiDiffColor = ".diffuseColor"  # type double3
            self.aiDiffWeight = ".diffuseStrength"
            self.aiDiffRoughness = "diffuseRoughtness"

            self.aiSpecColor = ".specular1Color"  # type double3
            self.aiSpecWeight = ".specular1Strength"
            self.aiSpecRoughness = ".specular1Roughness"
            self.aiSpecFresnel = ".specular1FresnelMode"
            self.aiFresnel_Coe = ".specular1Ior"

            self.aiBump = ".normalCamera"

            self.aiEmissionColor = ".emissionColor"
            self.aiEmissionScale = ".emissionStrength"

            self.aiTransparencyList = [".opacityR", ".opacityG", ".opacityB"]


##
## Module Function
##

if __name__ == "__main__":
    pass
