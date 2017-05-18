import os
import sys

import maya.cmds as cmds
import yaml

cmds.loadPlugin('AbcExport.mll', quiet=True)
cmds.loadPlugin('AbcImport.mll', quiet=True)

# adding plugins path
root_path = os.path.dirname(yaml.__file__)
root_path = os.path.abspath(os.path.join(os.path.dirname(root_path),".."))

path = os.path.join(root_path, 'Maya', 'plugins')
os.environ['MAYA_PLUG_IN_PATH'] += ';%s' % path.replace('\\', '/')

path = os.path.join(root_path, 'Maya', 'plugins', '2017')
os.environ['MAYA_PLUG_IN_PATH'] += ';%s' % path.replace('\\', '/')

# adding python path
path = os.path.join(path, 'Maya', 'pythonpath')
sys.path.append(path.replace('\\', '/'))


# importing Tapp
cmds.evalDeferred('import Tapp')
