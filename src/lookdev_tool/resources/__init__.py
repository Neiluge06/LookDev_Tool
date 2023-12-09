import os
from PySide2 import QtCore

QtCore.QDir.addSearchPath('icons', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons/'))
QtCore.QDir.addSearchPath('grounds', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'grounds/'))
QtCore.QDir.addSearchPath('camera', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'camera/'))
QtCore.QDir.addSearchPath('hdri', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hdri/'))
QtCore.QDir.addSearchPath('preferences', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'preferences/'))

a = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'camera/')

