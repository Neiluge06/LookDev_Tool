from maya import cmds


def createFileText(fileName):
    """
    Creates File node from texture file
    :return: File node's name
    """
    # create file node
    fileNode = cmds.createNode('file', name=fileName, skipSelect=True)
    return fileNode


def changeColorSpace(colorSpace):
    """
    Change Maya's color space
    :param colorSpace: ColorSpace combo box from Qmenu

    """
    cmds.colorManagementPrefs(renderingSpaceName=colorSpace, edit=True)


def createTurn(numberOfFrames):
    """
    Creates tunTable with X numbers of frames

    The first half of number's frame is used to turn the camera's offset group, and the second half to turn the
    offset's group light.
    :param numberOfFrames: Numbers of frame from QLineEdit
    """

    if not cmds.objExists('Cam_Main_Grp') or not cmds.objExists('Lights_Grp'):
        raise RuntimeError('TurnTable function needs camera and lights in scene')

    else:
        # clear previous keys
        cmds.cutKey('Cam_Main_Grp', clear=True)
        cmds.cutKey('Lights_Grp', clear=True)

        # set keys
        cmds.setKeyframe('Cam_Main_Grp', attribute='rotateY', time=1, value=0, inTangentType='linear')
        cmds.setKeyframe('Cam_Main_Grp', attribute='rotateY', time=numberOfFrames / 2.0, value=360, inTangentType='linear', outTangentType='linear')
        cmds.setKeyframe('Lights_Grp', attribute='rotateY', time=numberOfFrames / 2.0, value=0, inTangentType='linear', outTangentType='linear')
        cmds.setKeyframe('Lights_Grp', attribute='rotateY', time=float(numberOfFrames), value=360, inTangentType='linear', outTangentType='linear')


def toggleColorPalette():
    """
    Hide the colorpalette, simple hide function from maya
    """
    if not cmds.objExists('Cam_Main_Grp'):
        raise RuntimeError(' Camera not in scene ')

    cmds.setAttr('ColorPalette_ALL_Grp.visibility', not cmds.getAttr('ColorPalette_ALL_Grp.visibility'))