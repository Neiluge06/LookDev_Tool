import os
from maya import cmds


TOOL_NAME = "Js_LookDev_Tool"
COLORSPACE_LIST = cmds.colorManagementPrefs(query=True, renderingSpaceNames=True)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
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
