import maya.cmds as cmds
import maya.mel as mel
import os
from shutil import move
import sys

def fkSwitch():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    #error checking for selection count
    sel=cmds.ls(selection=True)
    
    if len(sel)>=1:
        for selNode in sel:
            #travel upstream and finding the module
            obj=cmds.listConnections('%s.metaParent' % selNode,type='network')
            temp=cmds.listConnections('%s.metaParent' % obj[0],type='network')
            module=temp[0]
            
            #array for while loop
            metaNodes=list()
            
            #finding the anim controls and align FK to IK
            for node in cmds.listConnections('%s.message' % module):
                if (cmds.attributeQuery('component',n=node,ex=True))==True and (cmds.getAttr('%s.component' % node))=='extra':
                    FKIK=cmds.listConnections('%s.message' % node)
                    
                    if cmds.nodeType(FKIK[0])=='transform':
                        cmds.setAttr('%s.FKIK' % FKIK[0],0)
                    if cmds.nodeType(FKIK[1])=='transform':
                        cmds.setAttr('%s.FKIK' % FKIK[1],0)
                
                #cycle through module connections and find controls with switches
                if (cmds.attributeQuery('switch',n=node,ex=True))==True:
                    switch=cmds.listConnections('%s.switch' % node)
                    
                    if cmds.getAttr('%s.system' % node)=='fk' and switch!='':
                        metaNodes.append(node)
            
            #while loop to ensure switch order is correct
            index=1
            while index<=len(metaNodes):
                for o in metaNodes:
                    if cmds.getAttr('%s.index' % o)==index:
                        newNode=cmds.listConnections('%s.message' % o,type='transform')[0]
                        newSwitch=cmds.listConnections('%s.switch' % o,type='transform')[0]
                        
                        rot=cmds.xform(newSwitch,query=True,worldSpace=True,rotation=True)
                        cmds.xform(newNode,worldSpace=True,rotation=(rot[0],rot[1],rot[2]))
                        
                        if cmds.getAttr('%s.tx' % newNode,lock=True)==False:
                            pos=cmds.xform(newSwitch,query=True,worldSpace=True,translation=True)
                            cmds.xform(newNode,worldSpace=True,translation=(pos[0],pos[1],pos[2]))
                
                index+=1
    else:
        raise RuntimeError, 'Nothing is selected!'
    
    cmds.undoInfo(closeChunk=True)

def ikSwitch():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    #error checking for selection count
    sel=cmds.ls(selection=True)
    
    if len(sel)>=1:
        for selNode in sel:
            #travel upstream and finding the module
            obj=cmds.listConnections('%s.metaParent' % selNode,type='network')
            temp=cmds.listConnections('%s.metaParent' % obj[0],type='network')
            module=temp[0]
            
            #finding the anim controls and align IK to FK
            for node in cmds.listConnections('%s.message' % module,type='network'):
                #setting blend to IK
                if (cmds.attributeQuery('component',n=node,ex=True))==True and (cmds.getAttr('%s.component' % node))=='extra':
                    FKIK=cmds.listConnections('%s.message' % node)
                    
                    if cmds.nodeType(FKIK[0])=='transform':
                        cmds.setAttr('%s.FKIK' % FKIK[0],1)
                    if cmds.nodeType(FKIK[1])=='transform':
                        cmds.setAttr('%s.FKIK' % FKIK[1],1)
                
                if (cmds.attributeQuery('switch',n=node,ex=True))==True:
                    #cycle through module connections and finding controls with switches
                    switch=cmds.listConnections('%s.switch' % node)
                    
                    if cmds.getAttr('%s.system' % node)=='ik' and switch!='':
                        cnt=cmds.listConnections('%s.message' % node,type='transform')[0]
                        
                        pos=cmds.xform(switch,query=True,worldSpace=True,translation=True)
                        cmds.move(pos[0],pos[1],pos[2],cnt,worldSpace=True)
                        
                        if (cmds.attributeQuery('zero',n=node,ex=True))==True and (cmds.getAttr('%s.zero' % node))=='true':
                            cmds.xform(cnt,rotation=(0,0,0),objectSpace=True)
                        else:
                            rot=cmds.xform(switch,query=True,worldSpace=True,rotation=True)
                            cmds.xform(cnt,rotation=(rot[0],rot[1],rot[2]),worldSpace=True)
    else:
        raise RuntimeError, 'Nothing is selected!'
    
    cmds.undoInfo(closeChunk=True)

def selectLimb():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        for meta in cmds.listConnections('%s.message' % module,type='network'):
            if (cmds.attributeQuery('type',n=meta,ex=True))==True and (cmds.getAttr('%s.type' % meta))=='control':
                cmds.select(cmds.listConnections('%s.message' % meta,type='transform'),add=True)
    
    cmds.undoInfo(closeChunk=True)

def selectCharacter():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        root=rootFind(module)
        
        for cnt in childControls(root):
            cmds.select(cnt,add=True)
    
    cmds.undoInfo(closeChunk=True)
    
def rootFind(module):
    if (cmds.getAttr('%s.type' % module))=='root':
        return module
    else:
        return rootFind(cmds.listConnections('%s.metaParent' % module)[0])

def childControls(module):
    controls=list()
    
    for meta in cmds.listConnections('%s.message' % module,type='network'):
        if (cmds.getAttr('%s.type' % meta))=='control':
            controls+=cmds.listConnections('%s.message' % meta,type='transform')
        if (cmds.getAttr('%s.type' % meta))=='module':
            controls+=childControls(meta)
    
    return controls

def childModules(module):
    modules=list()
    
    for meta in cmds.listConnections('%s.message' % module,type='network'):
        if (cmds.getAttr('%s.type' % meta))=='module':
            modules.append(meta)
            modules+=childModules(meta)
    
    return modules

def keyLimb():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        for meta in cmds.listConnections('%s.message' % module,type='network'):
            if (cmds.attributeQuery('type',n=meta,ex=True))==True and (cmds.getAttr('%s.type' % meta))=='control':
                cmds.setKeyframe(cmds.listConnections('%s.message' % meta,type='transform'))
    
    cmds.undoInfo(closeChunk=True)

def keyCharacter():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        root=rootFind(module)
        
        for cnt in childControls(root):
            cmds.setKeyframe(cnt)
    
    cmds.undoInfo(closeChunk=True)

def smoothDisplay(node,smooth):
    if smooth:
        cmds.select(node)
        cmds.displaySmoothness(du=3,dv=3,pw=16,ps=4,po=3)
        cmds.subdivDisplaySmoothness(s=3)
        cmds.select(cl=True)
    else:
        cmds.select(node)
        cmds.displaySmoothness(du=0,dv=0,pw=4,ps=1,po=1)
        cmds.subdivDisplaySmoothness(s=1)
        cmds.select(cl=True)

def zeroNode(node):
    if (cmds.getAttr('%s.tx' % node,lock=True))!=True:
        cmds.setAttr('%s.tx' % node,0)
    if (cmds.getAttr('%s.ty' % node,lock=True))!=True:
        cmds.setAttr('%s.ty' % node,0)
    if (cmds.getAttr('%s.tz' % node,lock=True))!=True:
        cmds.setAttr('%s.tz' % node,0)
    if (cmds.getAttr('%s.rx' % node,lock=True))!=True:
        cmds.setAttr('%s.rx' % node,0)
    if (cmds.getAttr('%s.ry' % node,lock=True))!=True:
        cmds.setAttr('%s.ry' % node,0)
    if (cmds.getAttr('%s.rz' % node,lock=True))!=True:
        cmds.setAttr('%s.rz' % node,0)

def zeroControl():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    #getting selection
    sel=cmds.ls(sl=True)
    
    #zero controls
    for node in cmds.ls(sl=True):
        zeroNode(node)
    
    #revert selection
    cmds.select(sel)
    
    
    cmds.undoInfo(closeChunk=True)

def zeroLimb():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    #getting selection
    sel=cmds.ls(sl=True)
    
    #zero limb
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        for meta in cmds.listConnections('%s.message' % module,type='network'):
            if (cmds.attributeQuery('type',n=meta,ex=True))==True and (cmds.getAttr('%s.type' % meta))=='control':
                zeroNode(cmds.listConnections('%s.message' % meta,type='transform')[0])
    
    #revert selection
    cmds.select(sel)
    
    cmds.undoInfo(closeChunk=True)

def zeroCharacter():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    #getting selection
    sel=cmds.ls(sl=True)
    
    #zero character
    selectCharacter()
    
    for meta in cmds.ls(type='network'):
        if (cmds.attributeQuery('type',n=meta,ex=True))==True and (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('component',n=meta,ex=True))==True and cmds.getAttr('%s.component' % meta)=='world':
            worldCNT=cmds.listConnections('%s.message' % meta,type='transform')[0]
    
    cmds.select(worldCNT,deselect=True)
    
    zeroControl()
    
    #revert selection
    cmds.select(sel)
    
    cmds.undoInfo(closeChunk=True)

def highRezRig():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    proxyNodes=list()
    for node in cmds.ls(type='network'):
        if (cmds.attributeQuery('type',n=node,ex=True))==True and (cmds.getAttr('%s.type' % node))=='proxy':
            proxyNodes.append(cmds.listConnections('%s.message' % node,type='transform')[0])
    
    for node in cmds.ls(type='network'):
        if (cmds.attributeQuery('type',n=node,ex=True))==True and (cmds.getAttr('%s.type' % node))=='skin':
            geo=cmds.listConnections('%s.message' % node,type='transform')[0]
            
            cmds.setAttr('%s.visibility' % geo,True)
            midRez=True
            smoothDisplay(geo,True)
            
    for node in proxyNodes:
        cmds.setAttr('%s.visibility' % node,False)
        smoothDisplay(node,False)
    
    cmds.undoInfo(closeChunk=True)

def midRezRig():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    proxyNodes=list()
    for node in cmds.ls(type='network'):
        if (cmds.attributeQuery('type',n=node,ex=True))==True and (cmds.getAttr('%s.type' % node))=='proxy':
            proxyNodes.append(cmds.listConnections('%s.message' % node,type='transform')[0])
    
    for node in cmds.ls(type='network'):
        if (cmds.attributeQuery('type',n=node,ex=True))==True and (cmds.getAttr('%s.type' % node))=='skin':
            geo=cmds.listConnections('%s.message' % node,type='transform')[0]
            
            cmds.setAttr('%s.visibility' % geo,True)
            midRez=True
            smoothDisplay(geo,False)
            
    for node in proxyNodes:
        cmds.setAttr('%s.visibility' % node,False)
        smoothDisplay(node,False)
    
    cmds.undoInfo(closeChunk=True)

def lowRezRig():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    skinNodes=list()
    for node in cmds.ls(type='network'):
        if (cmds.attributeQuery('type',n=node,ex=True))==True and (cmds.getAttr('%s.type' % node))=='skin':
            skinNodes.append(cmds.listConnections('%s.message' % node,type='transform')[0])
    
    for node in cmds.ls(type='network'):
        if (cmds.attributeQuery('type',n=node,ex=True))==True and (cmds.getAttr('%s.type' % node))=='proxy':
            geo=cmds.listConnections('%s.message' % node,type='transform')[0]
            
            cmds.setAttr('%s.visibility' % geo,True)
            lowRez=True
            smoothDisplay(geo,False)
    
    for node in skinNodes:
        cmds.setAttr('%s.visibility' % node,False)
        smoothDisplay(node,False)
    
    cmds.undoInfo(closeChunk=True)

def flipLimb():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    neckList=list()
    fingerList=list()
    
    sel=cmds.ls(sl=True)
    
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        if cmds.getAttr('%s.component' % module)=='neck':
            moduleSide=cmds.getAttr('%s.side' % module)
            moduleComponent=cmds.getAttr('%s.component' % module)
            moduleIndex=cmds.getAttr('%s.index' % module)
            
            moduleControls=list()
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==False:
                    moduleControls.append(meta)
                if (cmds.getAttr('%s.type' % meta))=='plug':
                    plug=cmds.listConnections('%s.message' % meta,type='transform')
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==True:
                    moduleControls.append(meta)
            
            root=rootFind(module)
            
            for meta in cmds.listConnections('%s.message' % root,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.getAttr('%s.component' % meta))=='world':
                    worldCNT=cmds.listConnections('%s.message' % meta,type='transform')[0]
            
            if moduleSide=='c':
                mirrorValues=list()
                
                for meta in moduleControls:
                    neckDict=dict()
                    
                    cnt=cmds.listConnections('%s.message' % meta,type='transform')[0]
                    
                    neckDict['cnt']=cnt
                    
                    # translation mirror            
                    # create group and align to obj
                    sourceNull=cmds.group(parent=worldCNT,empty=True)
                    
                    sourcePOS=cmds.xform(cnt,q=True,ws=True,translation=True)
                    
                    cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                    
                    # mirror null translation values
                    sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                    
                    cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                    
                    sourceMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                    
                    cmds.delete(sourceNull)
                    
                    neckDict['translation']=sourceMirrorPOS
                    
                    # rotation mirror
                    rot=cmds.xform(cnt,q=True,os=True,ro=True)
                    neckDict['rotation']=[(rot[0]*-1),rot[1],(rot[2]*-1)]
                    
                    #adding to neck list
                    neckList.append(neckDict)
                    
        if cmds.getAttr('%s.component' % module)=='finger':            
            moduleSide=cmds.getAttr('%s.side' % module)
            moduleComponent=cmds.getAttr('%s.component' % module)
            moduleIndex=cmds.getAttr('%s.index' % module)
            
            moduleControls=list()
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==False:
                    moduleControls.append(meta)
                if (cmds.getAttr('%s.type' % meta))=='plug':
                    plug=cmds.listConnections('%s.message' % meta,type='transform')
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==True:
                    moduleControls.append(meta)
            
            root=rootFind(module)
            
            for meta in cmds.listConnections('%s.message' % root,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.getAttr('%s.component' % meta))=='world':
                    worldCNT=cmds.listConnections('%s.message' % meta,type='transform')[0]
            
            if moduleSide=='c':
                mirrorValues=list()
                
                for meta in moduleControls:
                    fingerDict=dict()
                    
                    cnt=cmds.listConnections('%s.message' % meta,type='transform')[0]
                    
                    fingerDict['cnt']=cnt
                    
                    # translation mirror            
                    # create group and align to obj
                    sourceNull=cmds.group(parent=worldCNT,empty=True)
                    
                    sourcePOS=cmds.xform(cnt,q=True,ws=True,translation=True)
                    
                    cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                    
                    # mirror null translation values
                    sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                    
                    cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                    
                    sourceMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                    
                    cmds.delete(sourceNull)
                    
                    fingerDict['translation']=sourceMirrorPOS
                    
                    # rotation mirror
                    rot=cmds.xform(cnt,q=True,os=True,ro=True)
                    fingerDict['rotation']=[rot[0],rot[1],rot[2]]
                    
                    #adding to neck list
                    fingerList.append(fingerDict)
            else:
                if moduleSide=='l':
                    oppSide='r'
                else:
                    oppSide='l'
                
                for meta in childModules(rootFind(module)):
                    if (cmds.getAttr('%s.side' % meta))==oppSide and (cmds.getAttr('%s.component' % meta))==moduleComponent and (cmds.getAttr('%s.index' % meta))==moduleIndex:
                        oppModule=meta
                
                oppControls=list()
                for meta in cmds.listConnections('%s.message' % oppModule,type='network'):
                    if (cmds.getAttr('%s.type' % meta))=='control':
                        oppControls.append(meta)
                    if (cmds.getAttr('%s.type' % meta))=='plug':
                        oppPlug=cmds.listConnections('%s.message' % meta,type='transform')
                
                matchControls=list()
                for meta in moduleControls:
                    tempList=list()
                    tempList.append(meta)
                    for oppMeta in oppControls:
                        if (cmds.getAttr('%s.component' % meta))==(cmds.getAttr('%s.component' % oppMeta)):
                            if (cmds.attributeQuery('system',n=meta,ex=True))==True and (cmds.getAttr('%s.system' % meta))==(cmds.getAttr('%s.system' % oppMeta)):
                                if (cmds.attributeQuery('index',n=meta,ex=True))==True and (cmds.getAttr('%s.index' % meta))==(cmds.getAttr('%s.index' % oppMeta)):
                                    tempList.append(oppMeta)
                                elif (cmds.attributeQuery('index',n=meta,ex=True))==False:
                                    tempList.append(oppMeta)
                            elif (cmds.attributeQuery('system',n=meta,ex=True))==False:
                                tempList.append(oppMeta)
                    
                    matchControls.append(tempList)
                
                # create reference node
                ref=worldCNT
                
                # mirroring controls
                mirrorValues=list()
                
                for metaList in matchControls:
                    sourceDict=dict()
                    targetDict=dict()
                    
                    sourceDict['cnt']=cmds.listConnections('%s.message' % metaList[0],type='transform')[0]
                    targetDict['cnt']=cmds.listConnections('%s.message' % metaList[1],type='transform')[0]
                    
                    sourceCNT=cmds.listConnections('%s.message' % metaList[0],type='transform')[0]
                    targetCNT=cmds.listConnections('%s.message' % metaList[1],type='transform')[0]
                    
                    sourceDict['rotation']=cmds.xform(targetCNT,os=True,q=True,rotation=True)
                    targetDict['rotation']=cmds.xform(sourceCNT,os=True,q=True,rotation=True)
                    
                    fingerList.append(sourceDict)
                    fingerList.append(targetDict)
    
    cmds.select(sel)
    
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        moduleSide=cmds.getAttr('%s.side' % module)
        moduleComponent=cmds.getAttr('%s.component' % module)
        moduleIndex=cmds.getAttr('%s.index' % module)
        
        moduleControls=list()
        for meta in cmds.listConnections('%s.message' % module,type='network'):
            if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==False:
                moduleControls.append(meta)
            if (cmds.getAttr('%s.type' % meta))=='plug':
                plug=cmds.listConnections('%s.message' % meta,type='transform')
        for meta in cmds.listConnections('%s.message' % module,type='network'):
            if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==True:
                moduleControls.append(meta)
        
        root=rootFind(module)
        
        for meta in cmds.listConnections('%s.message' % root,type='network'):
            if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.getAttr('%s.component' % meta))=='world':
                worldCNT=cmds.listConnections('%s.message' % meta,type='transform')[0]
        
        if moduleSide=='c':
            mirrorValues=list()
            
            for meta in moduleControls:
                cnt=cmds.listConnections('%s.message' % meta,type='transform')[0]
                
                # translation mirror            
                # create group and align to obj
                sourceNull=cmds.group(parent=worldCNT,empty=True)
                
                sourcePOS=cmds.xform(cnt,q=True,ws=True,translation=True)
                
                cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                
                # mirror null translation values
                sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                
                cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                
                sourceMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                
                mirrorValues.append(sourceMirrorPOS)
                
                cmds.delete(sourceNull)
                
            # using mirror values to mirror obj
            for count in xrange(0,len(moduleControls)):
                cnt=cmds.listConnections('%s.message' % moduleControls[count],type='transform')[0]
                
                cmds.xform(cnt,ws=True,translation=mirrorValues[count])
            
                # rotation mirror
                rot=cmds.xform(cnt,q=True,os=True,ro=True)
                cmds.xform(cnt,os=True,ro=((rot[0]*-1),rot[1],(rot[2]*-1)))
        else:
            if moduleSide=='l':
                oppSide='r'
            else:
                oppSide='l'
            
            for meta in childModules(rootFind(module)):
                if (cmds.getAttr('%s.side' % meta))==oppSide and (cmds.getAttr('%s.component' % meta))==moduleComponent and (cmds.getAttr('%s.index' % meta))==moduleIndex:
                    oppModule=meta
            
            oppControls=list()
            for meta in cmds.listConnections('%s.message' % oppModule,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control':
                    oppControls.append(meta)
                if (cmds.getAttr('%s.type' % meta))=='plug':
                    oppPlug=cmds.listConnections('%s.message' % meta,type='transform')
            
            matchControls=list()
            for meta in moduleControls:
                tempList=list()
                tempList.append(meta)
                for oppMeta in oppControls:
                    if (cmds.getAttr('%s.component' % meta))==(cmds.getAttr('%s.component' % oppMeta)):
                        if (cmds.attributeQuery('system',n=meta,ex=True))==True and (cmds.getAttr('%s.system' % meta))==(cmds.getAttr('%s.system' % oppMeta)):
                            if (cmds.attributeQuery('index',n=meta,ex=True))==True and (cmds.getAttr('%s.index' % meta))==(cmds.getAttr('%s.index' % oppMeta)):
                                tempList.append(oppMeta)
                            elif (cmds.attributeQuery('index',n=meta,ex=True))==False:
                                tempList.append(oppMeta)
                        elif (cmds.attributeQuery('system',n=meta,ex=True))==False:
                            tempList.append(oppMeta)
                
                matchControls.append(tempList)
            
            # create reference node
            ref=worldCNT
            
            # mirroring controls
            mirrorValues=list()
            extraValues=list()
            
            for metaList in matchControls:
                sourceCNT=cmds.listConnections('%s.message' % metaList[0],type='transform')[0]
                targetCNT=cmds.listConnections('%s.message' % metaList[1],type='transform')[0]
                
                # translation mirror
                # create group and align to obj
                sourceNull=cmds.group(parent=ref,empty=True)
                
                sourcePOS=cmds.xform(sourceCNT,q=True,ws=True,translation=True)
                
                cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                
                # mirror null translation values
                sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                
                cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                
                sourceMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                
                cmds.delete(sourceNull)
                
                # create group and align to obj
                sourceNull=cmds.group(parent=ref,empty=True)
                
                sourcePOS=cmds.xform(targetCNT,q=True,ws=True,translation=True)
                
                cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                
                # mirror null translation values
                sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                
                cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                
                targetMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                
                cmds.delete(sourceNull)
                
                # adding mirror values to list
                tempList=list()
                
                tempList.append(sourceMirrorPOS)
                tempList.append(targetMirrorPOS)
                
                mirrorValues.append(tempList)
                
                #mirroring extra control values
                sourceList=list()
                targetList=list()
                
                if (cmds.getAttr('%s.component' % metaList[0]))=='extra':
                    for attr in cmds.listAnimatable(sourceCNT):
                        sourceList.append(cmds.getAttr(attr))
                    for attr in cmds.listAnimatable(targetCNT):
                        targetList.append(cmds.getAttr(attr))
                    
                    sourceAttrs=cmds.listAnimatable(sourceCNT)
                    targetAttrs=cmds.listAnimatable(targetCNT)
                    for count in xrange(0,len(cmds.listAnimatable(sourceCNT))):
                        cmds.setAttr(sourceAttrs[count],targetList[count])
                        cmds.setAttr(targetAttrs[count],sourceList[count])
            
            # using mirror values to mirror obj
            for count in xrange(0,len(matchControls)):
                sourceCNT=cmds.listConnections('%s.message' % matchControls[count][0],type='transform')[0]
                targetCNT=cmds.listConnections('%s.message' % matchControls[count][1],type='transform')[0]
                
                if (cmds.attributeQuery('system',n=matchControls[count][0],ex=True))==True and (cmds.getAttr('%s.system' % matchControls[count][0]))=='ik' and (cmds.attributeQuery('worldspace',n=matchControls[count][0],ex=True))==False:
                    cmds.xform(sourceCNT,ws=True,translation=mirrorValues[count][1])
                    cmds.xform(targetCNT,ws=True,translation=mirrorValues[count][0])
                
                # rotation mirror
                sourceROT=cmds.xform(sourceCNT,q=True,os=True,ro=True)
                targetROT=cmds.xform(targetCNT,q=True,os=True,ro=True)
                cmds.xform(targetCNT,os=True,ro=((sourceROT[0]*-1),sourceROT[1],(sourceROT[2]*-1)))
                cmds.xform(sourceCNT,os=True,ro=((targetROT[0]*-1),targetROT[1],(targetROT[2]*-1)))
    
    #compensating neck modules
    for node in neckList:
        cmds.xform(node['cnt'],ws=True,translation=node['translation'])
        
        cmds.xform(node['cnt'],os=True,ro=node['rotation'])
    
    #reverting to original selection
    cmds.select(sel)
    
    cmds.undoInfo(closeChunk=True)

def flipCharacter():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    #getting selection
    sel=cmds.ls(sl=True)
    
    #getting upstream nodes
    node=cmds.ls(sl=True)[0]
    
    meta=cmds.listConnections('%s.metaParent' % node)[0]
    module=cmds.listConnections('%s.metaParent' % meta)[0]
    
    root=rootFind(module)
    
    #getting one control node per module
    selectNodes=list()
    
    for module in childModules(root):
        controlNodes=list()
        
        if cmds.getAttr('%s.side' % module)!='r':
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control':
                    controlNodes.append(cmds.listConnections('%s.message' % meta,type='transform'))
        
            selectNodes.append(controlNodes[0])
    
    #clearing the selection and selecting one control per module
    cmds.select(cl=True)
    
    for node in selectNodes:
        cmds.select(node,tgl=True)
        
    #mirror limbs
    flipLimb()
    
    #reverting to original selection
    cmds.select(sel)
    
    cmds.undoInfo(closeChunk=True)

def mirrorLimb():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    neckList=list()
    fingerList=list()
    
    sel=cmds.ls(sl=True)
    
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        if cmds.getAttr('%s.component' % module)=='neck':
            moduleSide=cmds.getAttr('%s.side' % module)
            moduleComponent=cmds.getAttr('%s.component' % module)
            moduleIndex=cmds.getAttr('%s.index' % module)
            
            moduleControls=list()
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==False:
                    moduleControls.append(meta)
                if (cmds.getAttr('%s.type' % meta))=='plug':
                    plug=cmds.listConnections('%s.message' % meta,type='transform')
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==True:
                    moduleControls.append(meta)
            
            root=rootFind(module)
            
            for meta in cmds.listConnections('%s.message' % root,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.getAttr('%s.component' % meta))=='world':
                    worldCNT=cmds.listConnections('%s.message' % meta,type='transform')[0]
            
            if moduleSide=='c':
                mirrorValues=list()
                
                for meta in moduleControls:
                    neckDict=dict()
                    
                    cnt=cmds.listConnections('%s.message' % meta,type='transform')[0]
                    
                    neckDict['cnt']=cnt
                    
                    # translation mirror            
                    # create group and align to obj
                    sourceNull=cmds.group(parent=worldCNT,empty=True)
                    
                    sourcePOS=cmds.xform(cnt,q=True,ws=True,translation=True)
                    
                    cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                    
                    # mirror null translation values
                    sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                    
                    cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                    
                    sourceMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                    
                    cmds.delete(sourceNull)
                    
                    neckDict['translation']=sourceMirrorPOS
                    
                    # rotation mirror
                    rot=cmds.xform(cnt,q=True,os=True,ro=True)
                    neckDict['rotation']=[(rot[0]*-1),rot[1],(rot[2]*-1)]
                    
                    #adding to neck list
                    neckList.append(neckDict)
                    
        if cmds.getAttr('%s.component' % module)=='finger':            
            moduleSide=cmds.getAttr('%s.side' % module)
            moduleComponent=cmds.getAttr('%s.component' % module)
            moduleIndex=cmds.getAttr('%s.index' % module)
            
            moduleControls=list()
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==False:
                    moduleControls.append(meta)
                if (cmds.getAttr('%s.type' % meta))=='plug':
                    plug=cmds.listConnections('%s.message' % meta,type='transform')
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==True:
                    moduleControls.append(meta)
            
            root=rootFind(module)
            
            for meta in cmds.listConnections('%s.message' % root,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.getAttr('%s.component' % meta))=='world':
                    worldCNT=cmds.listConnections('%s.message' % meta,type='transform')[0]
            
            if moduleSide=='c':
                mirrorValues=list()
                
                for meta in moduleControls:
                    fingerDict=dict()
                    
                    cnt=cmds.listConnections('%s.message' % meta,type='transform')[0]
                    
                    fingerDict['cnt']=cnt
                    
                    # translation mirror            
                    # create group and align to obj
                    sourceNull=cmds.group(parent=worldCNT,empty=True)
                    
                    sourcePOS=cmds.xform(cnt,q=True,ws=True,translation=True)
                    
                    cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                    
                    # mirror null translation values
                    sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                    
                    cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                    
                    sourceMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                    
                    cmds.delete(sourceNull)
                    
                    fingerDict['translation']=sourceMirrorPOS
                    
                    # rotation mirror
                    rot=cmds.xform(cnt,q=True,os=True,ro=True)
                    fingerDict['rotation']=[rot[0],rot[1],rot[2]]
                    
                    #adding to neck list
                    fingerList.append(fingerDict)
            else:
                if moduleSide=='l':
                    oppSide='r'
                else:
                    oppSide='l'
                
                for meta in childModules(rootFind(module)):
                    if (cmds.getAttr('%s.side' % meta))==oppSide and (cmds.getAttr('%s.component' % meta))==moduleComponent and (cmds.getAttr('%s.index' % meta))==moduleIndex:
                        oppModule=meta
                
                oppControls=list()
                for meta in cmds.listConnections('%s.message' % oppModule,type='network'):
                    if (cmds.getAttr('%s.type' % meta))=='control':
                        oppControls.append(meta)
                    if (cmds.getAttr('%s.type' % meta))=='plug':
                        oppPlug=cmds.listConnections('%s.message' % meta,type='transform')
                
                matchControls=list()
                for meta in moduleControls:
                    tempList=list()
                    tempList.append(meta)
                    for oppMeta in oppControls:
                        if (cmds.getAttr('%s.component' % meta))==(cmds.getAttr('%s.component' % oppMeta)):
                            if (cmds.attributeQuery('system',n=meta,ex=True))==True and (cmds.getAttr('%s.system' % meta))==(cmds.getAttr('%s.system' % oppMeta)):
                                if (cmds.attributeQuery('index',n=meta,ex=True))==True and (cmds.getAttr('%s.index' % meta))==(cmds.getAttr('%s.index' % oppMeta)):
                                    tempList.append(oppMeta)
                                elif (cmds.attributeQuery('index',n=meta,ex=True))==False:
                                    tempList.append(oppMeta)
                            elif (cmds.attributeQuery('system',n=meta,ex=True))==False:
                                tempList.append(oppMeta)
                    
                    matchControls.append(tempList)
                
                # create reference node
                ref=worldCNT
                
                # mirroring controls
                mirrorValues=list()
                
                for metaList in matchControls:
                    sourceDict=dict()
                    targetDict=dict()
                    
                    sourceDict['cnt']=cmds.listConnections('%s.message' % metaList[0],type='transform')[0]
                    targetDict['cnt']=cmds.listConnections('%s.message' % metaList[1],type='transform')[0]
                    
                    sourceCNT=cmds.listConnections('%s.message' % metaList[0],type='transform')[0]
                    targetCNT=cmds.listConnections('%s.message' % metaList[1],type='transform')[0]
                    
                    sourceDict['rotation']=cmds.xform(targetCNT,os=True,q=True,rotation=True)
                    targetDict['rotation']=cmds.xform(sourceCNT,os=True,q=True,rotation=True)
                    
                    fingerList.append(targetDict)
    
    cmds.select(sel)
    
    for node in cmds.ls(sl=True):
        meta=cmds.listConnections('%s.metaParent' % node)[0]
        module=cmds.listConnections('%s.metaParent' % meta)[0]
        
        moduleSide=cmds.getAttr('%s.side' % module)
        moduleComponent=cmds.getAttr('%s.component' % module)
        moduleIndex=cmds.getAttr('%s.index' % module)
        
        moduleControls=list()
        for meta in cmds.listConnections('%s.message' % module,type='network'):
            if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==False:
                moduleControls.append(meta)
            if (cmds.getAttr('%s.type' % meta))=='plug':
                plug=cmds.listConnections('%s.message' % meta,type='transform')
        for meta in cmds.listConnections('%s.message' % module,type='network'):
            if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.attributeQuery('system',n=meta,ex=True))==True:
                moduleControls.append(meta)
        
        root=rootFind(module)
        
        for meta in cmds.listConnections('%s.message' % root,type='network'):
            if (cmds.getAttr('%s.type' % meta))=='control' and (cmds.getAttr('%s.component' % meta))=='world':
                worldCNT=cmds.listConnections('%s.message' % meta,type='transform')[0]
        
        if moduleSide=='c':
            mirrorValues=list()
            
            for meta in moduleControls:
                cnt=cmds.listConnections('%s.message' % meta,type='transform')[0]
                
                # translation mirror            
                # create group and align to obj
                sourceNull=cmds.group(parent=worldCNT,empty=True)
                
                sourcePOS=cmds.xform(cnt,q=True,ws=True,translation=True)
                
                cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                
                # mirror null translation values
                sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                
                cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                
                sourceMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                
                mirrorValues.append(sourceMirrorPOS)
                
                cmds.delete(sourceNull)
                
            # using mirror values to mirror obj
            for count in xrange(0,len(moduleControls)):
                cnt=cmds.listConnections('%s.message' % moduleControls[count],type='transform')[0]
                
                cmds.xform(cnt,ws=True,translation=mirrorValues[count])
            
                # rotation mirror
                rot=cmds.xform(cnt,q=True,os=True,ro=True)
                cmds.xform(cnt,os=True,ro=((rot[0]*-1),rot[1],(rot[2]*-1)))
        else:
            if moduleSide=='l':
                oppSide='r'
            else:
                oppSide='l'
            
            for meta in childModules(rootFind(module)):
                if (cmds.getAttr('%s.side' % meta))==oppSide and (cmds.getAttr('%s.component' % meta))==moduleComponent and (cmds.getAttr('%s.index' % meta))==moduleIndex:
                    oppModule=meta
            
            oppControls=list()
            for meta in cmds.listConnections('%s.message' % oppModule,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control':
                    oppControls.append(meta)
                if (cmds.getAttr('%s.type' % meta))=='plug':
                    oppPlug=cmds.listConnections('%s.message' % meta,type='transform')
            
            matchControls=list()
            for meta in moduleControls:
                tempList=list()
                tempList.append(meta)
                for oppMeta in oppControls:
                    if (cmds.getAttr('%s.component' % meta))==(cmds.getAttr('%s.component' % oppMeta)):
                        if (cmds.attributeQuery('system',n=meta,ex=True))==True and (cmds.getAttr('%s.system' % meta))==(cmds.getAttr('%s.system' % oppMeta)):
                            if (cmds.attributeQuery('index',n=meta,ex=True))==True and (cmds.getAttr('%s.index' % meta))==(cmds.getAttr('%s.index' % oppMeta)):
                                tempList.append(oppMeta)
                            elif (cmds.attributeQuery('index',n=meta,ex=True))==False:
                                tempList.append(oppMeta)
                        elif (cmds.attributeQuery('system',n=meta,ex=True))==False:
                            tempList.append(oppMeta)
                
                matchControls.append(tempList)
            
            # create reference node
            ref=worldCNT
            
            # mirroring controls
            mirrorValues=list()
            extraValues=list()
            
            for metaList in matchControls:
                sourceCNT=cmds.listConnections('%s.message' % metaList[0],type='transform')[0]
                targetCNT=cmds.listConnections('%s.message' % metaList[1],type='transform')[0]
                
                # translation mirror
                # create group and align to obj
                sourceNull=cmds.group(parent=ref,empty=True)
                
                sourcePOS=cmds.xform(sourceCNT,q=True,ws=True,translation=True)
                
                cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                
                # mirror null translation values
                sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                
                cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                
                sourceMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                
                cmds.delete(sourceNull)
                
                # create group and align to obj
                sourceNull=cmds.group(parent=ref,empty=True)
                
                sourcePOS=cmds.xform(targetCNT,q=True,ws=True,translation=True)
                
                cmds.xform(sourceNull,ws=True,translation=sourcePOS)
                
                # mirror null translation values
                sourceNullPOS=cmds.xform(sourceNull,os=True,q=True,translation=True)
                
                cmds.xform(sourceNull,os=True,translation=((sourceNullPOS[0]*-1),sourceNullPOS[1],sourceNullPOS[2]))
                
                targetMirrorPOS=cmds.xform(sourceNull,ws=True,q=True,translation=True)
                
                cmds.delete(sourceNull)
                
                # adding mirror values to list
                tempList=list()
                
                tempList.append(sourceMirrorPOS)
                tempList.append(targetMirrorPOS)
                
                mirrorValues.append(tempList)
                
                #mirroring extra control values
                sourceList=list()
                targetList=list()
                
                if (cmds.getAttr('%s.component' % metaList[0]))=='extra':
                    for attr in cmds.listAnimatable(sourceCNT):
                        sourceList.append(cmds.getAttr(attr))
                    for attr in cmds.listAnimatable(targetCNT):
                        targetList.append(cmds.getAttr(attr))
                    
                    sourceAttrs=cmds.listAnimatable(sourceCNT)
                    targetAttrs=cmds.listAnimatable(targetCNT)
                    for count in xrange(0,len(cmds.listAnimatable(sourceCNT))):
                        cmds.setAttr(targetAttrs[count],sourceList[count])
            
            # using mirror values to mirror obj
            for count in xrange(0,len(matchControls)):
                sourceCNT=cmds.listConnections('%s.message' % matchControls[count][0],type='transform')[0]
                targetCNT=cmds.listConnections('%s.message' % matchControls[count][1],type='transform')[0]
                
                if (cmds.attributeQuery('system',n=matchControls[count][0],ex=True))==True and (cmds.getAttr('%s.system' % matchControls[count][0]))=='ik' and (cmds.attributeQuery('worldspace',n=matchControls[count][0],ex=True))==False:
                    cmds.xform(targetCNT,ws=True,translation=mirrorValues[count][0])
                
                # rotation mirror
                sourceROT=cmds.xform(sourceCNT,q=True,os=True,ro=True)
                targetROT=cmds.xform(targetCNT,q=True,os=True,ro=True)
                cmds.xform(targetCNT,os=True,ro=((sourceROT[0]*-1),sourceROT[1],(sourceROT[2]*-1)))
    
    #compensating neck modules
    for node in neckList:
        cmds.xform(node['cnt'],ws=True,translation=node['translation'])
        
        cmds.xform(node['cnt'],os=True,ro=node['rotation'])
    
    #reverting to original selection
    cmds.select(sel)
    
    cmds.undoInfo(closeChunk=True)

def mirrorCharacter():
    #undo enable
    cmds.undoInfo(openChunk=True)
    
    #getting selection
    sel=cmds.ls(sl=True)
    
    #getting upstream nodes
    node=cmds.ls(sl=True)[0]
    
    meta=cmds.listConnections('%s.metaParent' % node)[0]
    module=cmds.listConnections('%s.metaParent' % meta)[0]
    
    root=rootFind(module)
    
    #getting one control node per module
    selectNodes=list()
    
    for module in childModules(root):
        controlNodes=list()
        
        if cmds.getAttr('%s.side' % module)!='r':
            for meta in cmds.listConnections('%s.message' % module,type='network'):
                if (cmds.getAttr('%s.type' % meta))=='control':
                    controlNodes.append(cmds.listConnections('%s.message' % meta,type='transform'))
        
            selectNodes.append(controlNodes[0])
    
    #clearing the selection and selecting one control per module
    cmds.select(cl=True)
    
    for node in selectNodes:
        cmds.select(node,tgl=True)
        
    #mirror limbs
    mirrorLimb()
    
    #reverting to original selection
    cmds.select(sel)
    
    cmds.undoInfo(closeChunk=True)