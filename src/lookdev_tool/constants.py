import os
from maya import cmds


TOOL_NAME = "Js_LookDev_Tool"
COLORSPACE_LIST = cmds.colorManagementPrefs(query=True, renderingSpaceNames=True)
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
LIGHT_DOME_PATH = os.path.join(BASE_PATH, 'resources/hdri')
HDR_EXTENSIONS = ('exr', 'hdr')

ARNOLD_PREFERENCE_PATH = os.path.join(BASE_PATH, 'resources/preferences/arnoldPrefs.json')
VRAY_PREFERENCE_PATH = os.path.join(BASE_PATH, 'resources/preferences/vrayPrefs.json')

VRAY_LIGHT_VALUES = \
    (
        {
            'fillLight': {

            },
        },
        {
            'keyLight': {

            },
        },
        {
            'backLight': {

            },
        }
    )

ARNOLD_LIGHT_VALUES =\
    (
        {
            'fillLight': {

            },
        },
        {
            'keyLight': {

            },
        },
        {
            'backLight': {

            },
        }
    )
