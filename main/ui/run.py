"""
Run the emulation of the robot.
Author: Benjamin Dodd (1901386)
"""
from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_button import Button
from .ui_debug import Debug
from .ui_display import Ui_Display
from .ui_main import Ui_MainWindow
from .ui_mock_gpio import Ui_Board
from .ui_motor import Ui_Motor
from .ui_worker_manager import Ui_WorkerManager

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main window for the application
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setupSubwindows()
        self.mdiArea.tileSubWindows()

    def setupSubwindows(self):
        """
        Setup the subwindows
        """
        self.setupButtonSubWindow()
        self.setupDebugSubWindow()

    def setupButtonSubWindow(self):
        """
        Setup the button subwindow
        """
        button = Button("Main", 37)
        buttonSubWindow = QtWidgets.QMdiSubWindow()
        buttonSubWindow.setWidget(button)
        buttonSubWindow.setWindowTitle("Button")
        buttonSubWindow.setFixedHeight(button.height() + 30)
        buttonSubWindow.setFixedWidth(button.width() + 10)
        # set flags to prevent closing
        buttonSubWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.mdiArea.addSubWindow(buttonSubWindow)

    def setupDebugSubWindow(self):
        """
        Setup the debug subwindow
        """
        debug = Debug("Debug")
        debugSubWindow = QtWidgets.QMdiSubWindow()
        debugSubWindow.setWidget(debug)
        debugSubWindow.setWindowTitle("Debug")
        debugSubWindow.setFixedHeight(debug.height() + 30)
        debugSubWindow.setFixedWidth(debug.width() + 10)
        # set flags to prevent closing
        debugSubWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.mdiArea.addSubWindow(debugSubWindow)

