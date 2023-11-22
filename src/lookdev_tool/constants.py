import os
from maya import cmds


TOOL_NAME = "Js_LookDev_Tool"
COLORSPACE_LIST = cmds.colorManagementPrefs(query=True, renderingSpaceNames=True)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GROUND_1_PATH = ''
GROUND_2_PATH = ''
GROUND_3_PATH = ''
COLOR_CHECKER_PATH = ''


def setGroundPath(renderEngine):
    global GROUND_1_PATH
    GROUND_1_PATH = os.path.join(BASE_PATH, 'resources/grounds/ground_1_{}.ma'.format(renderEngine))

    global GROUND_2_PATH
    GROUND_2_PATH = os.path.join(BASE_PATH, 'resources/grounds/ground_2_{}.ma'.format(renderEngine))

    global GROUND_3_PATH
    GROUND_3_PATH = os.path.join(BASE_PATH, 'resources/grounds/ground_3_{}.ma'.format(renderEngine))


def setColorCheckerPath(renderEngine):
    global COLOR_CHECKER_PATH
    COLOR_CHECKER_PATH = os.path.join(BASE_PATH, 'resources/camera/ColorPalette_{}.ma'.format(renderEngine))


LIGHT_DOME_PATH = os.path.join(BASE_PATH, 'resources/hdri')

PREFERENCE_PATH = os.path.join(BASE_PATH, 'resources/preferences/prefs.json')

LIGHT_VALUES = \
            (
                {
                    'fillLight': dict(),
                },
                {
                    'keyLight': dict(),
                },
                {
                    'backLight':dict(),
                }
            )
