# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\motor.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Motor(object):
    def setupUi(self, Motor):
        Motor.setObjectName("Motor")
        Motor.resize(144, 144)
        self.gridLayout = QtWidgets.QGridLayout(Motor)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Motor)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.motorDial = QtWidgets.QDial(self.groupBox)
        self.motorDial.setMaximum(360)
        self.motorDial.setWrapping(True)
        self.motorDial.setNotchTarget(15.0)
        self.motorDial.setNotchesVisible(True)
        self.motorDial.setObjectName("motorDial")
        self.verticalLayout.addWidget(self.motorDial)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Motor)
        QtCore.QMetaObject.connectSlotsByName(Motor)

    def retranslateUi(self, Motor):
        _translate = QtCore.QCoreApplication.translate
        Motor.setWindowTitle(_translate("Motor", "Motor"))
        self.groupBox.setTitle(_translate("Motor", "Motor Name"))