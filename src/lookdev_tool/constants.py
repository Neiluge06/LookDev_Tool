import os
from maya import cmds


TOOL_NAME = "Js_LookDev_Tool"
COLORSPACE_LIST = cmds.colorManagementPrefs(query=True, renderingSpaceNames=True)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
GROUND_1_PATH = os.path.join(BASE_PATH, 'resources/grounds/ground_1.ma')
GROUND_2_PATH = os.path.join(BASE_PATH, 'resources/grounds/ground_2.ma')
GROUND_3_PATH = os.path.join(BASE_PATH, 'resources/grounds/ground_3.ma')

COLOR_CHECKER_PATH = os.path.join(BASE_PATH, 'resources/camera/ColorPalette.ma')
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
