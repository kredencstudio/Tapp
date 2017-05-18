# import os
# import sys

import maya.cmds as cmds

# import shutil

#testing ATOM

#import statement
print 'Tapp.Maya imported!'

#creating menu
import menu
reload(menu)


# #setting project
# cmds.evalDeferred('import Tapp.Maya.utils.setProject')

# #opening Tapp
# cmds.evalDeferred('import Tapp.Maya.gui as gui;win=gui.Window();win.show()')

# #import Red9
# sys.path.append(os.path.dirname(__file__))
# cmds.evalDeferred('import Tapp.Maya.Red9;Tapp.Maya.Red9.start()')
