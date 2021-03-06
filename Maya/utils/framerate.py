import maya.cmds as cmds


def FrameratePrompt():

    framerate = cmds.currentUnit(q=True, time=True)

    if framerate != 'pal':
        message = 'Maya session is not working with 25 fps.\n'
        message += 'Do you want to switch to 25 fps?'
        result = cmds.confirmDialog(title='FRAMERATE', message=message,
                                  icon='warning', backgroundColor=(0.5, 0, 0))

        if result == 'Confirm':

            cmds.currentUnit(time='pal')

scriptJobNum = cmds.scriptJob(event=('SceneOpened', FrameratePrompt))
