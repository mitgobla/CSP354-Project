"""
Run the emulation of the robot.
Author: Benjamin Dodd (1901386)
"""
from PyQt5 import QtCore, QtGui, QtWidgets

from .ui_button import Button
from .ui_debug import Debug
from .ui_display import Display
from .ui_main import Ui_MainWindow
from .ui_mock_gpio import BoardWindow
from .ui_motor import Motor
from .ui_worker_manager import Ui_WorkerManager

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    Main window for the application
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setupSubwindows()
        # self.mdiArea.tileSubWindows()

    def setupSubwindows(self):
        """
        Setup the subwindows
        """
        self.setupButtonSubWindow()
        self.setupDebugSubWindow()
        self.setupDisplaySubWindow("Right Display")
        self.setupDisplaySubWindow("Left Display")
        self.setupBoardSubWindow()
        self.setupMotorSubWindow()

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
        debugSubWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.mdiArea.addSubWindow(debugSubWindow)

    def setupDisplaySubWindow(self, name: str):
        """
        Setup the display subwindow
        """
        display = Display(name)
        displaySubWindow = QtWidgets.QMdiSubWindow()
        displaySubWindow.setWidget(display)
        displaySubWindow.setWindowTitle("Display")
        displaySubWindow.setFixedHeight(display.height() + 30)
        displaySubWindow.setFixedWidth(display.width() + 10)
        displaySubWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.mdiArea.addSubWindow(displaySubWindow)

    def setupBoardSubWindow(self):
        """
        Setup the GPIO board subwindow
        """
        board = BoardWindow()
        boardSubWindow = QtWidgets.QMdiSubWindow()
        boardSubWindow.setWidget(board)
        boardSubWindow.setWindowTitle("GPIO Board")
        boardSubWindow.setFixedHeight(board.height() + 30)
        boardSubWindow.setFixedWidth(board.width() + 10)
        boardSubWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.mdiArea.addSubWindow(boardSubWindow)

    def setupMotorSubWindow(self):
        """
        Setup the motor subwindow
        """
        motor = Motor("Stepper Motor")
        motorSubWindow = QtWidgets.QMdiSubWindow()
        motorSubWindow.setWidget(motor)
        motorSubWindow.setWindowTitle("Motor")
        motorSubWindow.setFixedHeight(motor.height() + 30)
        motorSubWindow.setFixedWidth(motor.width() + 10)
        motorSubWindow.setWindowFlags(QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
        self.mdiArea.addSubWindow(motorSubWindow)

