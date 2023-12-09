import maya.mel as mel
import os
import json
import logging

from maya import cmds

from lookdev_tool import lookdev_core
from lookdev_tool import constants

VRAY_CORE_LOGGER = logging.getLogger(__name__)
VRAY_CORE_LOGGER.setLevel(10)


class GroundClass(object):
    def __init__(self, path1, path2, path3, colorCheckerPath):
        self.path1 = path1
        self.path2 = path2
        self.path3 = path3
        self.colorCheckerPath = colorCheckerPath

    def setGround(self, index):
        """
        Set ground and delete if one is already set
        :param index: Combo box current floor

        """
        VRAY_CORE_LOGGER.debug('self.path1: {}, self.path2: {}, self.path3: {}'.format(self.path1, self.path2, self.path3))

        # import ground 1
        if index == 0:
            if cmds.objExists('ground_1_vray_ALL_Grp'):
                cmds.file(self.path1, removeReference=True)
            else:
                cmds.file(self.path1, reference=True)

                if cmds.objExists('ground_2_vray_ALL_Grp'):
                    cmds.file(self.path2, removeReference=True)

                if cmds.objExists('ground_3_vray_ALL_Grp'):
                    cmds.file(self.path3, removeReference=True)

        # import ground 2
        if index == 1:
            if cmds.objExists('ground_2_vray_ALL_Grp'):
                cmds.file(self.path2, removeReference=True)
            else:
                cmds.file(self.path2, reference=True)

                if cmds.objExists('ground_1_vray_ALL_Grp'):
                    cmds.file(self.path1, removeReference=True)

                if cmds.objExists('ground_3_vray_ALL_Grp'):
                    cmds.file(self.path3, removeReference=True)

        # import ground 3
        if index == 2:
            if cmds.objExists('ground_3_vray_ALL_Grp'):
                cmds.file(self.path3, removeReference=True)
            else:
                cmds.file(self.path3, reference=True)

                if cmds.objExists('ground_1_vray_ALL_Grp'):
                    cmds.file(self.path1, removeReference=True)

                if cmds.objExists('ground_2_vray_ALL_Grp'):
                    cmds.file(self.path2, removeReference=True)

        cmds.select(clear=True)


class LightDome(object):

    @staticmethod
    def setLightDome(hdriName):
        """
        Set light dome and delete it if one is already set
        :param hdriName: HDRI's name from QlineEdit
        """

        # query vRay plugin
        if not cmds.pluginInfo('vrayformaya.mll', query=True, loaded=True):
            raise RuntimeError('vRay plugin not loaded')

        if not cmds.objExists('lightDome'):
            lightDome = cmds.createNode('VRayLightDomeShape', name='lightDome', skipSelect=True)
            lightDomeFile = lookdev_core.createFileText('dome1')
            cmds.setAttr('{}.{}'.format(lightDome, 'useDomeTex'), 1)
            cmds.setAttr('{}.{}'.format(lightDomeFile, 'fileTextureName'), '{}.exr'.format(os.path.join(constants.LIGHT_DOME_PATH, hdriName)), type='string')
            cmds.setAttr('{}.{}'.format(lightDome, 'invisible'), 1)
            cmds.connectAttr('{}.{}'.format(lightDomeFile, 'outColor'), '{}.{}'.format(lightDome, 'domeTex'))

        else:
            lightDelOne = cmds.listConnections('dome1', source=True)
            lightDelTwo = cmds.listConnections(lightDelOne[-1], source=True)

            cmds.delete(lightDelTwo[1:])
            cmds.delete(lightDelOne[-1])

    @staticmethod
    def changeDome1Intens(value):
        """
        Changes lightDom intensity
        """
        cmds.setAttr('lightDome.intensityMult', value)

    @staticmethod
    def rotateDome(value):
        """
        Changes lightDom rotation
        """
        domeText = cmds.listConnections('VRayLightDome1', connections=True)

        cmds.setAttr('{}.{}'.format(domeText[1], 'horRotation'), value)


def createLight(name, intensity, translates, rotates):
    """
    Creates light function
    :return: None
    """
    # query vRay plugin
    if not cmds.pluginInfo('vrayformaya.mll', query=True, loaded=True):

        raise RuntimeError('vRay plugin not loaded')

    # create key light and rename the transform
    keyLight = cmds.createNode('VRayLightRectShape', name=name, skipSelect=True)

    keyLightnewTransform = cmds.rename(cmds.listRelatives(keyLight, parent=True), name+'Transform')

    # set light scale and intensity
    cmds.setAttr('{}.{}'.format(keyLightnewTransform, 'uSize'), 14)
    cmds.setAttr('{}.{}'.format(keyLightnewTransform, 'vSize'), 10)

    cmds.setAttr('{}.{}'.format(keyLight, 'intensity'), intensity)

    # place the light in front of the asset
    cmds.xform(keyLightnewTransform, translation=translates, rotation=rotates)

    # add ramp to the light
    cmds.setAttr('{}.{}'.format(keyLight, 'useRectTex'), 1)

    rampText = cmds.createNode('place2dTexture', name='keyLightText', skipSelect=True)
    rampKeyL = cmds.createNode('ramp', name='keyLightRamp', skipSelect=True)

    cmds.connectAttr('{}.{}'.format(rampText, 'outUV'), '{}.{}'.format(rampKeyL, 'uv'))
    cmds.connectAttr('{}.{}'.format(rampText, 'outUvFilterSize'), '{}.{}'.format(rampKeyL, 'uvFilterSize'))
    cmds.connectAttr('{}.{}'.format(rampKeyL, 'outColor'), '{}.{}'.format(keyLight, 'rectTex'))

    # set the ramp
    cmds.setAttr('{}.{}'.format(rampKeyL, 'colorEntryList[0].color'),  1, 1, 1, type='double3')
    cmds.setAttr('{}.{}'.format(rampKeyL, 'colorEntryList[1].color'), 0, 0, 0, type='double3')
    cmds.setAttr('{}.{}'.format(rampKeyL, 'colorEntryList[1].position'), 1)
    cmds.setAttr('{}.{}'.format(rampKeyL, 'type'), 4)
    cmds.setAttr('{}.{}'.format(rampKeyL, 'interpolation'), 3)


def setThreePointsLights():
    """
    Set Three points light in scene and delete them is they are already in scene
    """
    if cmds.objExists('fillLightTransform') and cmds.objExists('keyLightTransform') and cmds.objExists('backLightTransform'):
        cmds.delete('Lights_Grp')

    else:
        createLight('fillLight', 10, (-27.622, 13.845, 39.553), (-9.131, -33.499, 0))
        createLight('keyLight', 40, (42.354, 14.693, 24.781), (-11.178, 58.981, 0))
        createLight('backLight', 10, (17.813, 11.919, -29.204), (-10.897, -213.093, 0))

        # make lights invisible
        cmds.setAttr('{}.{}'.format('fillLight', 'invisible'), 1)
        cmds.setAttr('{}.{}'.format('keyLight', 'invisible'), 1)
        cmds.setAttr('{}.{}'.format('backLight', 'invisible'), 1)

        lightGroup = cmds.createNode('transform', name='Lights_Grp', skipSelect=True)

        cmds.parent('fillLightTransform', lightGroup)
        cmds.parent('keyLightTransform', lightGroup)
        cmds.parent('backLightTransform', lightGroup)

        cmds.select(clear=True)


def rotLights(rotation):
    """
    Set rotations on the light's offset group
    """
    if cmds.objExists('Lights_Grp'):
        cmds.setAttr('Lights_Grp.rotateY', rotation)


def changeLightIntensity(light, intensity):
    """
    Changes fill light intensity if it's in scene
    """
    if cmds.objExists('Lights_Grp'):
        cmds.setAttr('{}.intensity'.format(light), intensity)


def createCam(colorCheckerPath):
    """
    Create camera in scene
    :param colorCheckerPath: path of colorchecker to reference it
    """
    cmds.select(clear=True)

    if not cmds.objExists('Cam_Main_Grp'):
        cmds.createNode('camera', name='Main_Cam', skipSelect=True)
        cameraTransfo = cmds.listRelatives('Main_Cam', parent=True)
        cameraOffset = cmds.createNode('transform', name='Camera_Offset', skipSelect=True)
        cmds.rename(cameraTransfo, 'Main_Cam_Transform')

        # create color palette
        cmds.file(colorCheckerPath, reference=True)

        # group cam
        cmds.parent('ColorPalette_vray_ALL_Grp', 'Main_Cam_Transform')
        cmds.parent('Main_Cam_Transform', cameraOffset)

        cmds.createNode('transform', name='Cam_Main_Grp', skipSelect=True)
        cmds.parent(cameraOffset, 'Cam_Main_Grp')

        # move cam
        cmds.xform('Main_Cam_Transform', translation=(0, 4.542, 13.729))

        # set physical camera
        mel.eval('vray addAttributesFromGroup |Cam_Main_Grp|Camera_Offset|Main_Cam_Transform|Main_Cam vray_cameraPhysical 1;')
        mel.eval('setAttr "Main_Cam.vrayCameraPhysicalExposure" 0;')

    else:
        cmds.file(colorCheckerPath, removeReference=True)
        cmds.delete('Cam_Main_Grp')

    cmds.select(clear=True)


def rotateCam(rotateValue):
    """
    Rotate cam's offset group
    :param rotateValue: rotate value from rotateCam's Qline
    """
    if cmds.objExists('Cam_Main_Grp'):
        cmds.setAttr('{}.{}'.format('Cam_Main_Grp', 'rotateY'), rotateValue)


def disableLight(light, state):
    """
    Disable fill light if it's in scene
    :parameters:
        light: query of light in maya scene
        state: state of the light
    """
    if cmds.objExists('Lights_Grp'):
        cmds.setAttr('{}.enabled'.format(light), state)


def storePrefs():
    """
    Creates a json and write coordinates to replace the lights
    """
    # create dict from lights position, values, intensity and scale

    if not cmds.objExists('fillLightTransform'):
        raise RuntimeError('No lights in scene')

    for index, light in enumerate(['fillLight', 'keyLight', 'backLight']):
        constants.LIGHT_VALUES[index].get(light, {})[f'{light}Coords'] = cmds.xform(f'{light}Transform', query=True, matrix=True)
        constants.LIGHT_VALUES[index].get(light, {})[f'{light}UScale'] = cmds.getAttr(f'{light}.uSize')
        constants.LIGHT_VALUES[index].get(light, {})[f'{light}VScale'] = cmds.getAttr(f'{light}.vSize')
        constants.LIGHT_VALUES[index].get(light, {})[f'{light}Intens'] = cmds.getAttr(f'{light}.intensityMult')

    with open(constants.PREFERENCE_PATH, 'w') as wFile:
        wFile.write(json.dumps(constants.LIGHT_VALUES, indent=4))


def clearScene(colorCheckerPath, ground1Path, ground2Path, ground3Path):
    """
    Clear all tool's nodes in scene
    :param colorCheckerPath: colorChecker's path
    :param ground1Path: ground1's path
    :param ground2Path: ground2's path
    :param ground3Path: ground3's path
    """
    # cam
    if cmds.objExists('Cam_Main_Grp'):
        cmds.file(colorCheckerPath, removeReference=True)
        cmds.delete('Cam_Main_Grp')

    # ground
    if cmds.objExists('ground_1_vray_ALL_Grp'):
        cmds.file(ground1Path, removeReference=True)

    if cmds.objExists('ground_2_vray_ALL_Grp'):
        cmds.file(ground2Path, removeReference=True)

    if cmds.objExists('ground_3_vray_ALL_Grp'):
        cmds.file(ground3Path, removeReference=True)

    # lights
    if cmds.objExists('Lights_Grp'):
        cmds.delete('Lights_Grp')

    # lightDome
    if cmds.objExists('VRayLightDome1'):
        # del connected nodes
        lightDelOne = cmds.listConnections('dome1', source=True)
        lightDelTwo = cmds.listConnections(lightDelOne[-1], source=True)

        cmds.delete(lightDelTwo[1:])
        cmds.delete(lightDelOne[-1])


def importPrefs(lightValues):
    """
    Read .json to set position, rotation, scale and intensity to three points light
    """
    with open(lightValues, 'r') as fileRead:
        lightDictLoad = json.load(fileRead)

        # set the position, scale and intensity
        for index, light in enumerate(['fillLight', 'keyLight', 'backLight']):
            cmds.xform(f'{light}Transform', matrix=(lightDictLoad[index].get(f'{light}', {}).get(f'{light}Coords')))
            cmds.setAttr(f'{light}.uSize', (lightDictLoad[index].get(f'{light}', {}).get(f'{light}UScale')))
            cmds.setAttr(f'{light}.vSize', (lightDictLoad[index].get(f'{light}', {}).get(f'{light}VScale')))
            cmds.setAttr(f'{light}.intensityMult', (lightDictLoad[index].get(f'{light}', {}).get(f'{light}Intens')))
