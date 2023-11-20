from PySide2 import QtWidgets, QtCore


class QHLine(QtWidgets.QFrame):
    """
    Separator from QHLine subclass
    """
    def __init__(self):
        super(QHLine, self).__init__()

        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class FloatSlider(QtWidgets.QSlider):
    """Subclass slider to get slider with float values"""
    def __init__(self):

        super(FloatSlider, self).__init__(QtCore.Qt.Horizontal)
        super().setMinimum(0.0)

    def value(self):
        return float(super().value()) /10

    def setMaximum(self, maximum):
        return super().setMaximum(maximum*10)