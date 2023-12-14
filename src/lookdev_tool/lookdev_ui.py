from maya import cmds
import json
import os

from PySide2 import QtCore, QtWidgets, QtGui

from lookdev_tool import vray_core
from lookdev_tool import arnold_core
from lookdev_tool import lookdev_core
from lookdev_tool.Utils import openMaya_utils
from lookdev_tool.Utils import widgets
from lookdev_tool import constants


class MainUi(QtWidgets.QDialog):
    """
    Main UI class
    """
    def __init__(self):
        super(MainUi, self).__init__(parent=openMaya_utils.maya_main_window(QtWidgets.QDialog))
        self.colorList = [] 
        self._buildUi()
        self.setRenderEngine()
        self.createComboBox()
        self._connectUi()
        self.resize(500, 240)
        self._setupUi()

        self.setWindowTitle(constants.TOOL_NAME)

    def _buildUi(self):

        # Buttons
        self.setDirectoryButton = QtWidgets.QPushButton('Find tool folder')
        self.setDirectoryButton.setIcon(QtGui.QIcon('icons:Folder.png'))
        self.createCamButton = QtWidgets.QPushButton('Create Camera')
        self.createCamButton.setFixedSize(150, 25)
        self.createLightButton = QtWidgets.QPushButton('Create three points light')
        self.createLightButton.setFixedSize(150, 25)
        self.setHdriButton = QtWidgets.QPushButton('Set HDRI')
        self.setFloorButton = QtWidgets.QPushButton('Create floor')
        self.toggleColorPaletteButton = QtWidgets.QPushButton('Hide color palette')
        self.createTurnButton = QtWidgets.QPushButton('Create turntable')
        self.storePrefsButton = QtWidgets.QPushButton('Store preferences')
        self.importPrefsButton = QtWidgets.QPushButton('Import preferences')
        self.clearSceneButton = QtWidgets.QPushButton('Clear scene')

        # ComboBox
        self.renderEngineCombo = QtWidgets.QComboBox()
        self.renderEngineCombo.addItem('Arnold')
        self.renderEngineCombo.addItem('VRay')
        self.setGroundMenu = QtWidgets.QComboBox()
        self.setGroundMenu.addItem('Studio')
        self.setGroundMenu.addItem('Bathtub')
        self.setGroundMenu.addItem('Simple floor')
        pal = self.setGroundMenu.palette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(50, 50, 50))
        self.setGroundMenu.setPalette(pal)
        self.setHdriMenu = QtWidgets.QComboBox()
        self.setHdriMenu.addItem('studio_small_09_4k')
        self.setHdriMenu.addItem('secluded_beach_4k')
        self.setHdriMenu.addItem('artist_workshop_4k')
        self.setHdriMenu.addItem('brown_photostudio_02_4k')
        self.setHdriMenu.addItem('scythian_tombs_puresky_4k')
        palTwo = self.setHdriMenu.palette()
        palTwo.setColor(QtGui.QPalette.Button, QtGui.QColor(50, 50, 50))
        self.setHdriMenu.setPalette(palTwo)

        # checkboxs
        self.fillLightCheckBox = QtWidgets.QCheckBox()
        self.fillLightCheckBox.setText('Enable')
        self.keyLightCheckBox = QtWidgets.QCheckBox()
        self.keyLightCheckBox.setText('Enable')
        self.backLightCheckBox = QtWidgets.QCheckBox()
        self.backLightCheckBox.setText('Enable')

        # Labels
        self.rotateCamTitle = QtWidgets.QLabel('Rotate camera')
        self.rotateCamTitle.setFixedSize(90, 10)
        self.rotateCamLabel = QtWidgets.QLineEdit('0')
        self.rotateCamLabel.setFixedSize(40, 20)
        self.rotateLightTitle = QtWidgets.QLabel('Rotate lights')
        self.rotateLightTitle.setFixedSize(90, 20)
        self.rotateLightLabel = QtWidgets.QLineEdit('0')
        self.rotateLightLabel.setFixedSize(40, 20)
        self.fillLightTitle = QtWidgets.QLabel('Fill light intensity')
        self.fillLightTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.fillLightLabel = QtWidgets.QLineEdit('0')
        self.fillLightLabel.setFixedSize(40, 20)
        self.keyLightTitle = QtWidgets.QLabel('Key light intensity')
        self.keyLightTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.keyLightLabel = QtWidgets.QLineEdit('0')
        self.keyLightLabel.setFixedSize(40, 20)
        self.hdriTitle = QtWidgets.QLabel('Set HDRI')
        self.hdriTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.backLightTitle = QtWidgets.QLabel('Back light intensity')
        self.backLightLabel = QtWidgets.QLineEdit('0')
        self.backLightLabel.setFixedSize(40, 20)
        self.floorTitle = QtWidgets.QLabel('Set Floor')
        self.floorTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lightDomeintenTitle = QtWidgets.QLabel('Light dome intensity')
        self.lightDomeintenTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lightDomeintensLabel = QtWidgets.QLineEdit('1')
        self.lightDomeintensLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lightDomeintensLabel.setMaximumWidth(40)
        self.lightDomeRotateTitle = QtWidgets.QLabel('Rotate LightDome')
        self.lightDomeRotateTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.lightDomeRotateLabel = QtWidgets.QLineEdit('0')
        self.lightDomeRotateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.lightDomeRotateLabel.setMaximumWidth(40)
        self.turnTableTitle = QtWidgets.QLabel('Number of frames')
        self.turnTableFrameLabel = QtWidgets.QLineEdit('120')

        # Sliders
        self.rotateCamSlider = widgets.FloatSlider(QtCore.Qt.Horizontal)
        self.rotateCamSlider.setTickInterval(1)
        self.rotateCamSlider.setMinimum(0)
        self.rotateCamSlider.setMaximum(360)
        self.rotateLightSlider = widgets.FloatSlider(QtCore.Qt.Horizontal)
        self.rotateLightSlider.setTickInterval(1)
        self.rotateLightSlider.setMinimum(0)
        self.rotateLightSlider.setMaximum(360)
        self.fillLightSlider = widgets.FloatSlider(QtCore.Qt.Horizontal)
        self.fillLightSlider.setValue(0)
        self.fillLightSlider.setMaximum(500)
        self.keyLightSlider = widgets.FloatSlider(QtCore.Qt.Horizontal)
        self.keyLightSlider.setValue(0)
        self.keyLightSlider.setMaximum(500)
        self.backLightSlider = widgets.FloatSlider(QtCore.Qt.Horizontal)
        self.backLightSlider.setValue(0)
        self.backLightSlider.setMaximum(500)
        self.lightDomeIntensSlider = widgets.FloatSlider(QtCore.Qt.Horizontal)
        self.lightDomeIntensSlider.setValue(1)
        self.lightDomeIntensSlider.setMaximum(10)
        self.lightDomeRotateSlider = widgets.FloatSlider(QtCore.Qt.Horizontal)
        self.lightDomeRotateSlider.setMaximum(360)
        self.lightDomeRotateSlider.setValue(0)

        # Separators
        self.sep1 = widgets.QHLine()
        self.sep2 = widgets.QHLine()
        self.sep3 = widgets.QHLine()
        self.sep4 = widgets.QHLine()
        self.sep5 = widgets.QHLine()
        self.sep6 = widgets.QHLine()
        self.sep7 = widgets.QHLine()
        self.sep8 = widgets.QHLine()
        self.sep9 = widgets.QHLine()
        self.sep10 = widgets.QHLine()
        self.sep11 = widgets.QHLine()
        self.sep12 = widgets.QHLine()
        self.sep13 = widgets.QHLine()
        self.sep14 = widgets.QHLine()
        self.sep15 = widgets.QHLine()
        self.sep16 = widgets.QHLine()

    def _setupUi(self):
        # Creation
        self.mainLayout = QtWidgets.QGridLayout(self)
        self.hLayout = QtWidgets.QHBoxLayout(self)
        self.hLayoutTwo = QtWidgets.QHBoxLayout()
        self.hLayoutThree = QtWidgets.QHBoxLayout()
        self.hLayoutFour = QtWidgets.QHBoxLayout()
        self.hLayoutFive = QtWidgets.QHBoxLayout()
        self.hLayoutSix = QtWidgets.QHBoxLayout()
        self.hLayoutSeven = QtWidgets.QHBoxLayout()
        self.hLayoutHeight = QtWidgets.QHBoxLayout()

        # Add widgets
        self.mainLayout.addWidget(self.renderEngineCombo, 0, 0)
        self.mainLayout.addWidget(self.colorSpaceMenu, 0, 1)
        self.mainLayout.addWidget(self.setDirectoryButton, 0, 2)
        self.mainLayout.addWidget(self.sep1, 1, 0)
        self.mainLayout.addWidget(self.createCamButton, 2, 0)
        self.hLayout.addWidget(self.rotateCamTitle)
        self.hLayout.addWidget(self.rotateCamLabel)
        self.mainLayout.addWidget(self.rotateCamSlider, 2, 2)
        self.mainLayout.addWidget(self.sep2, 3, 0)
        self.mainLayout.addWidget(self.sep3, 3, 1)
        self.mainLayout.addWidget(self.sep4, 3, 2)
        self.mainLayout.addWidget(self.createLightButton, 4, 0)
        self.hLayoutTwo.addWidget(self.rotateLightTitle)
        self.hLayoutTwo.addWidget(self.rotateLightLabel)
        self.mainLayout.addWidget(self.rotateLightSlider, 4, 2)
        self.hLayoutThree.addWidget(self.fillLightTitle)
        self.hLayoutThree.addWidget(self.fillLightLabel)
        self.mainLayout.addWidget(self.fillLightSlider, 5, 1)
        self.mainLayout.addWidget(self.fillLightCheckBox, 6, 0)
        self.hLayoutFour.addWidget(self.keyLightTitle)
        self.hLayoutFour.addWidget(self.keyLightLabel)
        self.mainLayout.addWidget(self.keyLightSlider, 7, 1)
        self.mainLayout.addWidget(self.keyLightCheckBox, 8, 0)
        self.hLayoutFive.addWidget(self.backLightTitle)
        self.hLayoutFive.addWidget(self.backLightLabel)
        self.mainLayout.addWidget(self.backLightSlider, 9, 1)
        self.mainLayout.addWidget(self.backLightCheckBox, 10, 0)
        self.mainLayout.addWidget(self.sep5, 11, 0)
        self.mainLayout.addWidget(self.sep6, 11, 1)
        self.mainLayout.addWidget(self.sep7, 11, 2)
        self.mainLayout.addWidget(self.floorTitle, 12, 0)
        self.mainLayout.addWidget(self.setGroundMenu, 12, 1)
        self.mainLayout.addWidget(self.setFloorButton, 12, 2)
        self.mainLayout.addWidget(self.sep8, 13, 0)
        self.mainLayout.addWidget(self.sep9, 13, 1)
        self.mainLayout.addWidget(self.sep10, 13, 2)
        self.mainLayout.addWidget(self.hdriTitle, 14, 0)
        self.mainLayout.addWidget(self.setHdriMenu, 14, 1)
        self.mainLayout.addWidget(self.setHdriButton, 14, 2)
        self.hLayoutSix.addWidget(self.lightDomeintenTitle)
        self.hLayoutSix.addWidget(self.lightDomeintensLabel)
        self.mainLayout.addWidget(self.lightDomeIntensSlider, 15, 1)
        self.hLayoutSeven.addWidget(self.lightDomeRotateTitle)
        self.hLayoutSeven.addWidget(self.lightDomeRotateLabel)
        self.mainLayout.addWidget(self.lightDomeRotateSlider, 16, 1)
        self.mainLayout.addWidget(self.sep11, 17, 0)
        self.mainLayout.addWidget(self.sep12, 17, 1)
        self.mainLayout.addWidget(self.sep13, 17, 2)
        self.mainLayout.addWidget(self.toggleColorPaletteButton, 18, 0)
        self.mainLayout.addWidget(self.createTurnButton, 18, 1)
        self.hLayoutHeight.addWidget(self.turnTableTitle)
        self.hLayoutHeight.addWidget(self.turnTableFrameLabel)
        self.mainLayout.addWidget(self.sep11, 20, 0)
        self.mainLayout.addWidget(self.sep12, 20, 1)
        self.mainLayout.addWidget(self.sep13, 20, 2)
        self.mainLayout.addWidget(self.storePrefsButton, 21, 0)
        self.mainLayout.addWidget(self.importPrefsButton, 21, 1)
        self.mainLayout.addWidget(self.sep14, 22, 0)
        self.mainLayout.addWidget(self.sep15, 22, 1)
        self.mainLayout.addWidget(self.sep16, 22, 2)
        self.mainLayout.addWidget(self.clearSceneButton, 23, 1)

        # set spacing, width, height, etc
        self.mainLayout.setVerticalSpacing(5)
        self.mainLayout.setColumnMinimumWidth(0, 100)
        self.mainLayout.setColumnMinimumWidth(1, 100)
        self.mainLayout.setColumnMinimumWidth(2, 100)

        # add layout
        self.mainLayout.addLayout(self.hLayout, 2, 1)
        self.mainLayout.addLayout(self.hLayoutTwo, 4, 1)
        self.mainLayout.addLayout(self.hLayoutThree, 5, 0)
        self.mainLayout.addLayout(self.hLayoutFour, 7, 0)
        self.mainLayout.addLayout(self.hLayoutFive, 9, 0)
        self.mainLayout.addLayout(self.hLayoutSix, 15, 0)
        self.mainLayout.addLayout(self.hLayoutSeven, 16, 0)
        self.mainLayout.addLayout(self.hLayoutHeight, 18, 2)

        self.clearSceneButton.setStyleSheet('color: white; background: darkRed')

    def _connectUi(self):
        self.renderEngineCombo.currentIndexChanged.connect(self.setRenderEngine)
        self.colorSpaceMenu.currentIndexChanged.connect(self.changeColorSpace)
        self.setDirectoryButton.clicked.connect(self.openBrowser)
        self.createCamButton.clicked.connect(self.sendToCreateCam)
        self.createCamButton.clicked.connect(self.resetRotateCamSlider)
        self.rotateCamSlider.valueChanged.connect(self.updateRotateCamValueFromSlider)
        self.rotateCamLabel.editingFinished.connect(self.changeRotateCamValueFromQline)
        self.createLightButton.clicked.connect(self.setThreePointsLights)
        self.createLightButton.clicked.connect(self.enableAllLights)
        self.rotateLightSlider.valueChanged.connect(self.rotateLightFromSlider)
        self.rotateLightLabel.editingFinished.connect(self.changeRotateLightLabelFromQline)
        self.setFloorButton.clicked.connect(self.setGround)
        self.fillLightSlider.valueChanged.connect(self.changeFillLightLabelFromSlider)
        self.fillLightLabel.editingFinished.connect(self.changeFillLightSliderFromQline)
        self.keyLightSlider.valueChanged.connect(self.changeKeyLightLabelFromSlider)
        self.keyLightLabel.editingFinished.connect(self.changeKeyLightFromQline)
        self.backLightLabel.editingFinished.connect(self.changeBackLightFromQline)
        self.backLightSlider.valueChanged.connect(self.changeBackLightFromSlider)
        self.fillLightCheckBox.stateChanged.connect(self.enableFillLight)
        self.keyLightCheckBox.stateChanged.connect(self.enableKeyLight)
        self.backLightCheckBox.stateChanged.connect(self.enableBackLight)
        self.setHdriButton.clicked.connect(self.setHdri)
        self.lightDomeintensLabel.editingFinished.connect(self.changeLightDomeItensFromQline)
        self.lightDomeIntensSlider.valueChanged.connect(self.changeLightDomeItensFromSlider)
        self.lightDomeRotateLabel.editingFinished.connect(self.changeLightDomerotateFromQline)
        self.lightDomeRotateSlider.valueChanged.connect(self.changeLightDomerotateFromSlider)
        self.toggleColorPaletteButton.clicked.connect(self.toggleColorPalette)
        self.createTurnButton.clicked.connect(self.createTurn)
        self.storePrefsButton.clicked.connect(self.storePrefs)
        self.importPrefsButton.clicked.connect(self.importPrefs)
        self.clearSceneButton.clicked.connect(self.clearScene)

    def createComboBox(self):
        """
        Creates a combo box with all colorSpaces available from Maya.
        """
        # comboBox
        self.colorSpaceMenu = QtWidgets.QComboBox()
        [self.colorSpaceMenu.addItem(colorSpace) for colorSpace in constants.COLORSPACE_LIST]

    def setRenderEngine(self):
        self.basePath = os.path.dirname(os.path.abspath(__file__))
        # Set witch module is used to send commands
        if self.renderEngineCombo.currentText() == 'VRay':
            self.renderEngine = vray_core
            self.lightDomeClass = self.renderEngine.LightDome()
            self.fillLight = 'fillLight'
            self.keyLight = 'keyLight'
            self.backLight = 'backLight'
            self.ground_1_path = QtCore.QDir.path(QtCore.QDir('grounds:ground_1_vray.ma'))
            self.ground_2_path = QtCore.QDir.path(QtCore.QDir('grounds:ground_2_vray.ma'))
            self.ground_3_path = QtCore.QDir.path(QtCore.QDir('grounds:ground_3_vray.ma'))
            self.color_checker_path = QtCore.QDir.path(QtCore.QDir('camera:ColorPalette_vray.ma'))
            self.groundClass = self.renderEngine.GroundClass(self.ground_1_path, self.ground_2_path, self.ground_3_path, self.color_checker_path)
            return

        self.renderEngine = arnold_core
        self.lightDomeClass = self.renderEngine.LightDome()
        self.fillLight = 'fillLightTransform'
        self.keyLight = 'keyLightTransform'
        self.backLight = 'backLightTransform'
        self.ground_1_path = QtCore.QDir.path(QtCore.QDir('grounds:ground_1_arnold.ma'))
        self.ground_2_path = QtCore.QDir.path(QtCore.QDir('grounds:ground_2_arnold.ma'))
        self.ground_3_path = QtCore.QDir.path(QtCore.QDir('grounds:ground_3_arnold.ma'))
        self.color_checker_path = QtCore.QDir.path(QtCore.QDir('camera:ColorPalette_arnold.ma'))

        self.groundClass = self.renderEngine.GroundClass(self.ground_1_path, self.ground_2_path, self.ground_3_path, self.color_checker_path)

    def sendToCreateCam(self):
        self.renderEngine.createCam(self.color_checker_path)

    def resetRotateCamSlider(self):
        """
        Reset the cam slider when cam is created
        """
        self.rotateCamLabel.setText('0')
        self.rotateCamSlider.setValue(0)

    def changeColorSpace(self):
        """
        Send change color space to Core
        """
#       # change Maya's color space in Core
        lookdev_core.changeColorSpace(self.colorSpaceMenu.currentText())

    @staticmethod
    def openBrowser():
        """
        open the browser to set another path to ground 1, 2, 3, colorChecker and prefs
        """
        groundDirectory = cmds.fileDialog2(fileFilter='*', fileMode=3, dialogStyle=2)

        constants.PREFERENCE_PATH = groundDirectory[0] + '/Preferences.txt'
        constants.LIGHT_DOME_PATH = groundDirectory[0] + '/'

    def updateRotateCamValueFromSlider(self):
        """
        changes the rotateCam label when slider is moved
        """
        # change rotateCam label value
        self.rotateCamLabel.setText(str(self.rotateCamSlider.value())[:6])

        # send rotateCam value to rotateCam in Core
        self.renderEngine.rotateCam(self.rotateCamSlider.value())

    def changeRotateCamValueFromQline(self):
        """
        Changes rotateCam label's value from slider
        """
        self.rotateCamSlider.setValue(float(self.rotateCamLabel.text()))

    def setThreePointsLights(self):
        """
        Send createLight to Core and reset sliders and lineedits
        """
        # send setThreePointsLight to Core
        self.renderEngine.setThreePointsLights()

        if not lookdev_core.queryExists('Lights_Grp'):
            self.rotateLightSlider.setValue(0)
            self.rotateLightLabel.setText('0')
            self.fillLightLabel.setText('0')
            self.fillLightSlider.setValue(0)
            self.keyLightSlider.setValue(0)
            self.keyLightLabel.setText('0')
            self.backLightSlider.setValue(0)
            self.backLightLabel.setText('0')

        else:
            # reset sliders and lineEdits
            self.rotateLightSlider.setValue(0)
            self.rotateLightLabel.setText('0')
            self.fillLightLabel.setText('10')
            self.fillLightSlider.setValue(10)
            self.keyLightSlider.setValue(40)
            self.keyLightLabel.setText('40')
            self.backLightSlider.setValue(10)
            self.backLightLabel.setText('10')

    def rotateLightFromSlider(self):
        """
        changes the rotateLight label when slider is moved and send it to Core
        """
        # change rotateCam label value
        self.rotateLightLabel.setText(str(self.rotateLightSlider.value())[:6])

        # send to Core
        self.renderEngine.rotLights(self.rotateLightSlider.value())

    def changeRotateLightLabelFromQline(self):
        """
        Changes rotateLight label's value from slider
        """
        self.rotateLightSlider.setValue(float(self.rotateLightLabel.text()))

    def setGround(self):
        """
        Send setGround to Core
        """
        self.groundClass.setGround(self.setGroundMenu.currentIndex())

    def changeFillLightLabelFromSlider(self):
        """
        Changes Fill light label from slider's value and send it to Core
        """
        self.fillLightLabel.setText(str(self.fillLightSlider.value())[:6])
        self.renderEngine.changeLightIntensity(self.fillLight, float(self.fillLightSlider.value()))

    def changeFillLightSliderFromQline(self):
        """
        Changes Fill light slider from label's value
        """
        self.fillLightSlider.setValue(float(self.fillLightLabel.text()))

    def changeKeyLightFromQline(self):
        """
        Changes key light label from slider's value
        """
        self.keyLightSlider.setValue(float(self.keyLightLabel.text()))

    def changeKeyLightLabelFromSlider(self):
        """
        Changes key light label from slider and send it to Core
        """
        self.keyLightLabel.setText(str(self.keyLightSlider.value())[:6])
        self.renderEngine.changeLightIntensity(self.keyLight, float(self.keyLightLabel.text()))

    def changeBackLightFromQline(self):
        """
        Changes back light slider from Qline'text
        """
        self.backLightSlider.setValue(float(self.backLightLabel.text()))

    def changeBackLightFromSlider(self):
        """
        Changes back light label from slider and send it to Core
        """
        self.backLightLabel.setText(str(self.backLightSlider.value()))
        self.renderEngine.changeLightIntensity(self.backLight, float(self.backLightLabel.text()))

    def enableAllLights(self):
        """
        Enable all lights when create light button is pressed
        """
        # fillLight
        if not lookdev_core.queryExists('Lights_Grp'):
            self.fillLightCheckBox.setChecked(False)

        else:
            self.fillLightCheckBox.setChecked(True)

        # keyLight
        if not lookdev_core.queryExists('Lights_Grp'):
            self.keyLightCheckBox.setChecked(False)

        else:
            self.keyLightCheckBox.setChecked(True)

        # backLight
        if not lookdev_core.queryExists('Lights_Grp'):
            self.backLightCheckBox.setChecked(False)

        else:
            self.backLightCheckBox.setChecked(True)

    def enableFillLight(self):
        """
        Send fill light enable to Core
        """
        self.renderEngine.disableLight(self.fillLight, self.fillLightCheckBox.isChecked())

    def enableKeyLight(self):
        """
        Send key light enable to Core
        """
        self.renderEngine.disableLight(self.keyLight, self.keyLightCheckBox.isChecked())

    def enableBackLight(self):
        """
        Send back light enable to Core
        """
        self.renderEngine.disableLight(self.backLight, self.backLightCheckBox.isChecked())

    def setHdri(self):
        """
        send set hdri with name to Core
        """
        self.lightDomeClass.setLightDome(self.setHdriMenu.currentText())

        # if HDRI exists, set lightDome's slider and Qline to 1
        if not lookdev_core.queryExists('JS_lightDome'):
            self.lightDomeRotateSlider.setValue(0)
            self.lightDomeRotateLabel.setText('0')
            self.lightDomeIntensSlider.setValue(0)
            self.lightDomeintensLabel.setText('0')

        else:
            self.lightDomeRotateSlider.setValue(0)
            self.lightDomeRotateLabel.setText('0')
            self.lightDomeIntensSlider.setValue(1)
            self.lightDomeintensLabel.setText('1')

    def changeLightDomeItensFromQline(self):
        """
        Changes lightDome slider from Qline's text
        """
        self.lightDomeIntensSlider.setValue(float(self.lightDomeintensLabel.text()))

    def changeLightDomeItensFromSlider(self):
        """
        Changes lightDome label from slider and send it to Core
        """
        self.lightDomeintensLabel.setText(str(self.lightDomeIntensSlider.value()))
        self.lightDomeClass.changeDome1Intens(float(self.lightDomeintensLabel.text()))

    def changeLightDomerotateFromQline(self):
        """
        Changes lightDome rotate slider from Qline's text
        """
        self.lightDomeRotateSlider.setValue(float(self.lightDomeRotateLabel.text()))

    def changeLightDomerotateFromSlider(self):
        """
        Changes lightDome rotate label from slider and send it to Core
        """
        self.lightDomeRotateLabel.setText(str(self.lightDomeRotateSlider.value()))
        self.lightDomeClass.rotateDome(float(self.lightDomeRotateLabel.text()))

    @staticmethod
    def toggleColorPalette():
        """
        Send hide color palette to Core
        """
        lookdev_core.toggleColorPalette()

    def createTurn(self):
        """
        Send createTurn to Core with numbers of frames in argument
        """
        lookdev_core.createTurn(int(self.turnTableFrameLabel.text()))

    def storePrefs(self):
        """
        Send store prefs to Core with light dictionnary in argument
        """
        # lights coordinates and intensity
        # add checkboxes values

        constants.LIGHT_VALUES[0].get(self.fillLight, {})['fillLightEnabled'] = self.fillLightCheckBox.isChecked()
        constants.LIGHT_VALUES[1].get(self.keyLight, {})['keyLightEnabled'] = self.keyLightCheckBox.isChecked()
        constants.LIGHT_VALUES[2].get(self.backLight, {})['backLightEnabled'] = self.backLightCheckBox.isChecked()

        self.renderEngine.storePrefs()

    def importPrefs(self):
        """
        Send import pref to Core with preference's path in argument and set the sliders
        """
        with open(constants.PREFERENCE_PATH, 'r') as oFile:
            fileReaded = json.load(oFile)

            #fillLight
            self.fillLightSlider.setValue(fileReaded[0].get('fillLight', {}).get('fillLightIntens'))
            self.fillLightCheckBox.setChecked(fileReaded[0].get('fillLight', {}).get('fillLightEnabled'))

            # keyLight
            self.keyLightSlider.setValue(fileReaded[1].get('keyLight', {}).get('keyLightIntens'))
            self.keyLightCheckBox.setChecked(fileReaded[1].get('keyLight', {}).get('keyLightEnabled'))

            # backLight
            self.backLightSlider.setValue(fileReaded[2].get('backLight', {}).get('backLightIntens'))
            self.backLightCheckBox.setChecked(fileReaded[2].get('backLight', {}).get('backLightEnabled'))

        self.renderEngine.importPrefs(constants.PREFERENCE_PATH)

    def clearScene(self):
        """
        Send clear scene to Core and reset light's sliders and labels"""
        self.renderEngine.clearScene(self.color_checker_path,
                                     self.ground_1_path,
                                     self.ground_2_path,
                                     self.ground_3_path
                                     )

        # reset sliders and labels
        self.fillLightCheckBox.setChecked(False)
        self.keyLightCheckBox.setChecked(False)
        self.backLightCheckBox.setChecked(False)
        self.rotateCamSlider.setValue(0)
        self.rotateLightSlider.setValue(0)
        self.rotateLightSlider.setValue(0)
        self.fillLightSlider.setValue(0)
        self.keyLightSlider.setValue(0)
        self.backLightSlider.setValue(0)
        self.lightDomeIntensSlider.setValue(0)
        self.lightDomeRotateSlider.setValue(0)
