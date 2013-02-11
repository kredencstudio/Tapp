import os
import sys

import maya.cmds as cmds

import Tapp.Maya.rigging.modules as modules
import Tapp.Maya.utils.meta as mum
import Tapp.Maya.rigging.config as mrc

def __importModule__(modulePath):
    f = os.path.basename( modulePath )
    d = os.path.dirname( modulePath )
 
    toks = f.split( '.' )
    modname = toks[0]
 
    # Check if dirrectory is really a directory
    if( os.path.exists( d ) ):
 
    # Check if the file directory already exists in the sys.path array
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(d == path):
                pathfound = 1
 
    # If the dirrectory is not part of sys.path add it
        if not pathfound:
            sys.path.append( d )
 
    # exec works like MEL's eval but you need to add in globals() 
    # at the end to make sure the file is imported into the global 
    # namespace else it will only be in the scope of this function
    exec ('import ' + modname+' as modules') in globals()

def Create(module):
    
    modulesPath=mrc.config['modules'].replace('\\','/')
    
    __importModule__(modulesPath+'/'+module+'.py')
    
    modules.Create()

def Rig():
    ''' Rigs all modules in the scene. '''
    
    modules=[]
    for meta in cmds.ls(type='network'):
        data=mum.GetData(meta)
        
        if data['type']=='root':
            modules.append(meta)
    
    for module in modules:
        __rig__(module)

def __rig__(module):
    ''' Rigs the provided module. '''
    
    data=mum.GetData(module)
    moduleName=data['component']
    
    modulesPath=mrc.config['modules'].replace('\\','/')
    
    __importModule__(modulesPath+'/'+moduleName+'.py')
    
    modules.Rig(module)