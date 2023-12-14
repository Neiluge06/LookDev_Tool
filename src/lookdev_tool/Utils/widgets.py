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
    def __init__(self, orientation):
        super().__init__(orientation)
        self.decimals = 4
        self._max_int = 10 ** self.decimals

        super().setMinimum(0)
        super().setMaximum(self._max_int)

        self._min_value = 0.0
        self._max_value = 100.0

    @property
    def _value_range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super().value()) / self._max_int * self._value_range + self._min_value

    def setValue(self, value):
        super().setValue(int((value - self._min_value) / self._value_range * self._max_int))

    def setMinimum(self, value):
        if value > self._max_value:
            raise ValueError("Minimum limit cannot be higher than maximum")

        self._min_value = value
        self.setValue(self.value())

    def setMaximum(self, value):
        if value < self._min_value:
            raise ValueError("Maximum limit cannot be smaller than minimum")

        self._max_value = value
        self.setValue(self.value())

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value
