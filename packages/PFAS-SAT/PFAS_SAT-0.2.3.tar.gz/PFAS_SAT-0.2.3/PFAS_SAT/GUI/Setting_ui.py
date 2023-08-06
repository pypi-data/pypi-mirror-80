# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Setting.ui',
# licensing of 'Setting.ui' applies.
#
# Created: Fri Sep 18 13:23:29 2020
#      by: pyside2-uic  running on PySide2 5.13.1
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Setting(object):
    def setupUi(self, Setting):
        Setting.setObjectName("Setting")
        Setting.resize(659, 488)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/ICONS/PFAS_SAT_1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Setting.setWindowIcon(icon)
        self.gridLayout_2 = QtWidgets.QGridLayout(Setting)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Setting)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.CutOff = QtWidgets.QLineEdit(Setting)
        self.CutOff.setObjectName("CutOff")
        self.gridLayout.addWidget(self.CutOff, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(Setting)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Setting)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.ErrorLimit = QtWidgets.QLineEdit(Setting)
        self.ErrorLimit.setObjectName("ErrorLimit")
        self.gridLayout.addWidget(self.ErrorLimit, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Setting)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Cancel = QtWidgets.QPushButton(Setting)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/ICONS/Remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Cancel.setIcon(icon1)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.Apply = QtWidgets.QPushButton(Setting)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/ICONS/Update.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Apply.setIcon(icon2)
        self.Apply.setObjectName("Apply")
        self.horizontalLayout.addWidget(self.Apply)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)

        self.retranslateUi(Setting)
        QtCore.QMetaObject.connectSlotsByName(Setting)

    def retranslateUi(self, Setting):
        Setting.setWindowTitle(QtWidgets.QApplication.translate("Setting", "PFAS SAT Setting", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Setting", "Cut-off:", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Setting", "Fraction of Total Incoming PFAS", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Setting", "Acceptable error limit:", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Setting", "%", None, -1))
        self.Cancel.setText(QtWidgets.QApplication.translate("Setting", "Cancel", None, -1))
        self.Apply.setText(QtWidgets.QApplication.translate("Setting", "Apply", None, -1))

from . import  PFAS_SAT_rc
