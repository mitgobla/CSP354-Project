# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\debug.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from logging import Handler
from PyQt5 import QtCore, QtGui, QtWidgets

from . import LOGGER

class Ui_Debug(object):
    def setupUi(self, Debug):
        Debug.setObjectName("Debug")
        Debug.resize(517, 341)
        self.gridLayout = QtWidgets.QGridLayout(Debug)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Debug)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.debugList = QtWidgets.QListWidget(self.groupBox)
        self.debugList.setObjectName("debugList")
        self.gridLayout_2.addWidget(self.debugList, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Debug)
        QtCore.QMetaObject.connectSlotsByName(Debug)

    def retranslateUi(self, Debug):
        _translate = QtCore.QCoreApplication.translate
        Debug.setWindowTitle(_translate("Debug", "Debug"))
        self.groupBox.setTitle(_translate("Debug", "Debug Title"))
        __sortingEnabled = self.debugList.isSortingEnabled()
        self.debugList.setSortingEnabled(False)
        self.debugList.setSortingEnabled(__sortingEnabled)
