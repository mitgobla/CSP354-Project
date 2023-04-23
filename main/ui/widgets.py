"""
Widgets for the main window.
Author: Benjamin Dodd (1901386)
"""

from logging import Handler
from PyQt5.QtWidgets import QWidget, QListWidgetItem
from PyQt5.QtGui import QPixmap

from . import LOGGER
from .ui_button import Ui_Button
from .ui_debug import Ui_Debug
from .ui_display import Ui_Display
from .ui_mock_gpio import Ui_Board
from .ui_motor import Ui_Motor
from .ui_worker_manager import Ui_WorkerManager

class Button(QWidget, Ui_Button):
    """
    Button widget
    """
    def __init__(self, name, pin, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.name = name
        self.pin = pin
        self.groupBox.setTitle(name)
        self.pushButton.setCheckable(True)
        self.pushButton.toggled.connect(self.button_toggled)

    def button_toggled(self, state):
        """
        Called when the button is toggled
        """
        LOGGER.debug("Button %s toggled to %s", self.name, state)

class Debug(QWidget, Ui_Debug):

    class DebugHandler(Handler):
        def __init__(self, debugWidget):
            super().__init__()
            self.debugWidget = debugWidget

        def emit(self, record):
            self.debugWidget.addDebug(record.getMessage())
    """
    Debug widget
    """
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.name = name
        self.groupBox.setTitle(name)

        # anytime a log message is posted, add it to the debug list
        self.debugHandler = Debug.DebugHandler(self)
        LOGGER.addHandler(self.debugHandler)

    def emit(self, record):
        self.addDebug(record.getMessage())

    def addDebug(self, text):
        item = QListWidgetItem()
        item.setText(text)
        self.debugList.addItem(text)
        self.debugList.scrollToBottom()

class Display(QWidget, Ui_Display):
    """
    Display widget
    """
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.name = name
        self.groupBox.setTitle(name)

    def set_image(self, image):
        """
        Set the image to display
        """
        self.image.setPixmap(QPixmap(image))

class BoardWindow(QWidget, Ui_Board):
    """
    GPIO Board Widget
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

class Motor(QWidget, Ui_Motor):
    """
    Motor widget
    """
    def __init__(self, name, parent=None):
        super(Motor, self).__init__(parent)
        self.setupUi(self)
        self.name = name
        self.groupBox.setTitle(name)
        self.motorDial.valueChanged.connect(self.value_changed)

    def value_changed(self, value):
        """
        Value changed
        """
        LOGGER.debug("Motor %s value changed to %s", self.name, value)

class WorkerManager(QWidget, Ui_WorkerManager):
    def __init__(self, parent=None):
        super(WorkerManager, self).__init__(parent)
        self.setupUi(self)

