import os
from PySide2 import QtCore

QtCore.QDir.addSearchPath('icons', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons/'))
