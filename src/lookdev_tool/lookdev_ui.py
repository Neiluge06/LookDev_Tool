from maya import cmds
import os

from PySide2 import QtCore, QtWidgets, QtGui

from lookdev_tool import vray_core
from lookdev_tool import arnold_core
from lookdev_tool import lookdev_core
from lookdev_tool.Utils.openMaya_utils import getMayaMainWindow
from lookdev_tool.Utils import widgets
from lookdev_tool import constants


class MainUi(QtWidgets.QDialog):
    """Main UI"""
    def __init__(self) -> None:
        super(MainUi, self).__init__(parent=getMayaMainWindow(QtWidgets.QDialog))

        self.colorList = [] 
        self._buildUi()
        self.setRenderEngine()
        self.createComboBox()
        self._connectUi()
        self._setupUi()
        self.queryHdr()

        self.setWindowTitle(constants.TOOL_NAME)

    def _buildUi(self) -> None:

        # Buttons
        self.setDirectoryButton = QtWidgets.QPushButton('Find tool folder')
        self.setDirectoryButton.setIcon(QtGui.QIcon('icons:Folder.png'))
        self.createCamButton = QtWidgets.QPushButton('Create Camera')
        self.createCamButton.setFixedSize(150, 25)
        self.createLightButton = QtWidgets.QPushButton('Create three points light')
        self.createLightButton.setFixedSize(150, 25)
        self.setHdriButton = QtWidgets.QPushButton('Set HDRI')
        self.setFloorButton = QtWidgets.QPushButton('Create floor')
        self.colorPaletteButton = QtWidgets.QPushButton('Hide color palette')
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

        palTwo = self.setHdriMenu.palette()
        palTwo.setColor(QtGui.QPalette.Button, QtGui.QColor(50, 50, 50))
        self.setHdriMenu.setPalette(palTwo)

        # checkboxes
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

    def _setupUi(self) -> None:
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
        self.mainLayout.addWidget(self.colorPaletteButton, 18, 0)
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
        self.resize(500, 240)

    def _connectUi(self) -> None:
        self.renderEngineCombo.currentIndexChanged.connect(self.setRenderEngine)
        self.colorSpaceMenu.currentIndexChanged.connect(self.onColorSpaceMenuCurrentIndexChanged)
        self.setDirectoryButton.clicked.connect(self.openBrowser)
        self.createCamButton.clicked.connect(self.sendToCreateCam)
        self.createCamButton.clicked.connect(self.resetRotateCamSlider)
        self.rotateCamSlider.valueChanged.connect(self.updateRotateCamValueFromSlider)
        self.rotateCamLabel.editingFinished.connect(self.changeRotateCamValueFromQline)
        self.createLightButton.clicked.connect(self.onCreateLightButtonClicked)
        self.createLightButton.clicked.connect(self.enableAllLights)
        self.rotateLightSlider.valueChanged.connect(self.onRotateLightSliderValueChanged)
        self.rotateLightLabel.editingFinished.connect(self.changeRotateLightLabelFromQline)
        self.setFloorButton.clicked.connect(self.onSetFloorButtonClicked)
        self.fillLightSlider.valueChanged.connect(self.onFillLightSliderValueChanged)
        self.fillLightLabel.editingFinished.connect(self.onFillLightLabelEditingFinished)
        self.keyLightSlider.valueChanged.connect(self.onKeyLightSliderValueChanged)
        self.keyLightLabel.editingFinished.connect(self.changeKeyLightFromQline)
        self.backLightLabel.editingFinished.connect(self.onBackLightLabelEditingFinished)
        self.backLightSlider.valueChanged.connect(self.changeBackLightFromSlider)
        self.fillLightCheckBox.stateChanged.connect(self.enableFillLight)
        self.keyLightCheckBox.stateChanged.connect(self.onKeyLightCheckBoxStateChanged)
        self.backLightCheckBox.stateChanged.connect(self.onBackLightCheckBoxStateChanged)
        self.setHdriButton.clicked.connect(self.onSetHdriButtonClicked)
        self.lightDomeintensLabel.editingFinished.connect(self.onLightDomeintensLabelEditingFinished)
        self.lightDomeIntensSlider.valueChanged.connect(self.onLightDomeIntensSliderValueChanged)
        self.lightDomeRotateLabel.editingFinished.connect(self.onLightDomeRotateLabelEditingFinished)
        self.lightDomeRotateSlider.valueChanged.connect(self.changeLightDomerotateFromSlider)
        self.colorPaletteButton.clicked.connect(self.onToggleColorPaletteButtonClicked)
        self.createTurnButton.clicked.connect(self.onCreateTurnButtonClicked)
        self.storePrefsButton.clicked.connect(self.onStorePrefsButtonClicked)
        self.importPrefsButton.clicked.connect(self.onImportPrefsButtonClicked)
        self.clearSceneButton.clicked.connect(self.onClearSceneButtonClicked)

    def createComboBox(self) -> None:
        """Creates a combo box with the Maya's colorSpaces."""
        self.colorSpaceMenu = QtWidgets.QComboBox()
        for colorSpace in constants.COLORSPACE_LIST:
            self.colorSpaceMenu.addItem(colorSpace)

    def queryHdr(self) -> None:
        """Adds the hrd present in hdr path"""
        for hdr in os.listdir(constants.LIGHT_DOME_PATH):
            if hdr.split('.')[-1] in constants.HDR_EXTENSIONS:
                self.setHdriMenu.addItem(hdr)

    def setRenderEngine(self) -> None:
        """Sets the render engine"""
        #TODO refactor this method to set the render engine's attributes in their respective module.
        self.basePath = os.path.dirname(os.path.abspath(__file__))

        # Set which module is used to send commands
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
            self.lightValues = constants.VRAY_LIGHT_VALUES
            self.colorpaletteName = 'ColorPalette_vray_ALL_Grp'
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
        self.lightValues = constants.ARNOLD_LIGHT_VALUES
        self.colorpaletteName = 'ColorPalette_arnold_ALL_Grp'

    def sendToCreateCam(self) -> None:
        """Triggers create cam function with the associated color path"""
        self.renderEngine.createCam(self.color_checker_path)

    def resetRotateCamSlider(self) -> None:
        """Reset the cam slider when cam is created"""
        self.rotateCamLabel.setText('0')
        self.rotateCamSlider.setValue(0)

    def onColorSpaceMenuCurrentIndexChanged(self) -> None:
        """Change the Maya's color space"""
        # change Maya's color space in Core
        lookdev_core.changeColorSpace(self.colorSpaceMenu.currentText())

    @staticmethod
    def openBrowser() -> None:
        """opens the browser to set a new ground and prefs path"""
        groundDirectory = cmds.fileDialog2(fileFilter='*', fileMode=3, dialogStyle=2)

        constants.PREFERENCE_PATH = groundDirectory[0] + '/Preferences.txt'
        constants.LIGHT_DOME_PATH = groundDirectory[0] + '/'

    def updateRotateCamValueFromSlider(self) -> None:
        """changes the rotateCam label when slider value is changed"""
        # change rotateCam label value
        self.rotateCamLabel.setText(str(self.rotateCamSlider.value())[:6])

        # send rotateCam value to rotateCam in Core
        self.renderEngine.rotateCam(self.rotateCamSlider.value())

    def changeRotateCamValueFromQline(self) -> None:
        """Changes rotateCam label's value from slider"""
        self.rotateCamSlider.setValue(float(self.rotateCamLabel.text()))

    def onCreateLightButtonClicked(self) -> None:
        """Create a three point lights in Maya's scene"""
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
            return

        # reset sliders and lineEdits
        self.rotateLightSlider.setValue(0)
        self.rotateLightLabel.setText('0')
        self.fillLightLabel.setText('10')
        self.fillLightSlider.setValue(10)
        self.keyLightSlider.setValue(40)
        self.keyLightLabel.setText('40')
        self.backLightSlider.setValue(10)
        self.backLightLabel.setText('10')

    def onRotateLightSliderValueChanged(self) -> None:
        """changes the rotateLight label when slider is moved and send it to Core"""
        # change rotateCam label value
        self.rotateLightLabel.setText(str(self.rotateLightSlider.value())[:6])

        # send to Core
        self.renderEngine.rotLights(self.rotateLightSlider.value())

    def changeRotateLightLabelFromQline(self) -> None:
        """Changes rotateLight label's value"""
        self.rotateLightSlider.setValue(float(self.rotateLightLabel.text()))

    def onSetFloorButtonClicked(self) -> None:
        """Sets a ground on Maya's scene"""
        self.groundClass.setGround(self.setGroundMenu.currentIndex())

    def onFillLightSliderValueChanged(self) -> None:
        """Changes Fill light label from slider's value and send it to Core"""
        self.fillLightLabel.setText(str(self.fillLightSlider.value())[:6])
        self.renderEngine.changeLightIntensity(self.fillLight, float(self.fillLightSlider.value()))

    def onFillLightLabelEditingFinished(self) -> None:
        """Changes Fill light slider's value"""
        self.fillLightSlider.setValue(float(self.fillLightLabel.text()))

    def changeKeyLightFromQline(self) -> None:
        """Changes key light label from slider's value"""
        self.keyLightSlider.setValue(float(self.keyLightLabel.text()))

    def onKeyLightSliderValueChanged(self) -> None:
        """Changes key light label from slider and send it to Core"""
        self.keyLightLabel.setText(str(self.keyLightSlider.value())[:6])
        self.renderEngine.changeLightIntensity(self.keyLight, float(self.keyLightLabel.text()))

    def onBackLightLabelEditingFinished(self) -> None:
        """Changes back light slider's value'"""
        self.backLightSlider.setValue(float(self.backLightLabel.text()))

    def changeBackLightFromSlider(self) -> None:
        """Changes back light label's value'"""
        self.backLightLabel.setText(str(self.backLightSlider.value()))
        self.renderEngine.changeLightIntensity(self.backLight, float(self.backLightLabel.text()))

    def enableAllLights(self) -> None:
        """Enables all lights when create light button is pressed"""
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

    def enableFillLight(self) -> None:
        """Send fill light enable to Core"""
        self.renderEngine.disableLight(self.fillLight, self.fillLightCheckBox.isChecked())

    def onKeyLightCheckBoxStateChanged(self) -> None:
        """Enables key light"""
        self.renderEngine.disableLight(self.keyLight, self.keyLightCheckBox.isChecked())

    def onBackLightCheckBoxStateChanged(self) -> None:
        """Enables back light"""
        self.renderEngine.disableLight(self.backLight, self.backLightCheckBox.isChecked())

    def onSetHdriButtonClicked(self) -> None:
        """Sets a HDR in Maya's scene"""
        self.lightDomeClass.setLightDome(self.setHdriMenu.currentText())

        # if HDRI exists, set lightDome's slider and Qline to 1
        if not lookdev_core.queryExists(self.lightDomeClass.LIGHT_DOME_NAME):
            self.lightDomeRotateSlider.setValue(0)
            self.lightDomeRotateLabel.setText('0')
            self.lightDomeIntensSlider.setValue(0)
            self.lightDomeintensLabel.setText('0')
            return

        self.lightDomeRotateSlider.setValue(0)
        self.lightDomeRotateLabel.setText('0')
        self.lightDomeIntensSlider.setValue(1)
        self.lightDomeintensLabel.setText('1')

    def onLightDomeintensLabelEditingFinished(self) -> None:
        """Changes lightDome slider's value"""
        self.lightDomeIntensSlider.setValue(float(self.lightDomeintensLabel.text()))

    def onLightDomeIntensSliderValueChanged(self) -> None:
        """Changes lightDome label from slider and send it to Core"""
        self.lightDomeintensLabel.setText(str(self.lightDomeIntensSlider.value()))
        self.lightDomeClass.changeDome1Intens(float(self.lightDomeintensLabel.text()))

    def onLightDomeRotateLabelEditingFinished(self) -> None:
        """Changes lightDome rotate slider's value'"""
        self.lightDomeRotateSlider.setValue(float(self.lightDomeRotateLabel.text()))

    def changeLightDomerotateFromSlider(self) -> None:
        """Changes lightDome rotate label's text and send it to Core"""
        self.lightDomeRotateLabel.setText(str(self.lightDomeRotateSlider.value()))
        self.lightDomeClass.rotateDome(float(self.lightDomeRotateLabel.text()))

    def onToggleColorPaletteButtonClicked(self) -> None:
        """Hide color palette group in Maya's scene"""
        lookdev_core.toggleColorPalette(self.colorpaletteName)

    def onCreateTurnButtonClicked(self) -> None:
        """Creates turn table in Maya"""
        lookdev_core.createTurn(int(self.turnTableFrameLabel.text()))

    def onStorePrefsButtonClicked(self) -> None:
        """Store preferences"""
        # lights coordinates and intensity
        self.lightValues[0].get(self.fillLight, {})['fillLightEnabled'] = self.fillLightCheckBox.isChecked()
        self.lightValues[1].get(self.keyLight, {})['keyLightEnabled'] = self.keyLightCheckBox.isChecked()
        self.lightValues[2].get(self.backLight, {})['backLightEnabled'] = self.backLightCheckBox.isChecked()

        self.renderEngine.storePrefs()

    def onImportPrefsButtonClicked(self) -> None:
        """Import preferences and sets lights values"""
        settings = self.renderEngine.importPrefs()

        #fillLight
        self.fillLightSlider.setValue(settings[0].get('fillLight', {}).get('fillLightIntens'))
        self.fillLightCheckBox.setChecked(settings[0].get('fillLight', {}).get('fillLightEnabled'))

        # keyLight
        self.keyLightSlider.setValue(settings[1].get('keyLight', {}).get('keyLightIntens'))
        self.keyLightCheckBox.setChecked(settings[1].get('keyLight', {}).get('keyLightEnabled'))

        # backLight
        self.backLightSlider.setValue(settings[2].get('backLight', {}).get('backLightIntens'))
        self.backLightCheckBox.setChecked(settings[2].get('backLight', {}).get('backLightEnabled'))

    def onClearSceneButtonClicked(self) -> None:
        """Clears scene and reset light's sliders and labels"""
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
