# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IR_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(450, 650)
        MainWindow.setMinimumSize(QtCore.QSize(450, 650))
        MainWindow.setMaximumSize(QtCore.QSize(450, 650))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.winBwImg = QtWidgets.QLabel(self.centralwidget)
        self.winBwImg.setGeometry(QtCore.QRect(225, 225, 200, 200))
        self.winBwImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winBwImg.setText("")
        self.winBwImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winBwImg.setScaledContents(True)
        self.winBwImg.setObjectName("winBwImg")
        self.winTemperatureImg = QtWidgets.QLabel(self.centralwidget)
        self.winTemperatureImg.setGeometry(QtCore.QRect(25, 25, 200, 200))
        self.winTemperatureImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winTemperatureImg.setText("")
        self.winTemperatureImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winTemperatureImg.setScaledContents(True)
        self.winTemperatureImg.setObjectName("winTemperatureImg")
        self.winMaskImg = QtWidgets.QLabel(self.centralwidget)
        self.winMaskImg.setGeometry(QtCore.QRect(25, 425, 200, 200))
        self.winMaskImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winMaskImg.setText("")
        self.winMaskImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winMaskImg.setScaledContents(True)
        self.winMaskImg.setObjectName("winMaskImg")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(240, 60, 75, 23))
        self.btnBrowse.setObjectName("btnBrowse")
        self.txtImgPth = QtWidgets.QLineEdit(self.centralwidget)
        self.txtImgPth.setGeometry(QtCore.QRect(240, 30, 180, 20))
        self.txtImgPth.setObjectName("txtImgPth")
        self.btnLoad = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoad.setGeometry(QtCore.QRect(345, 60, 75, 23))
        self.btnLoad.setObjectName("btnLoad")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setEnabled(True)
        self.label_4.setGeometry(QtCore.QRect(25, 225, 200, 200))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/Mask.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.btnMask = QtWidgets.QPushButton(self.centralwidget)
        self.btnMask.setGeometry(QtCore.QRect(140, 390, 75, 23))
        self.btnMask.setObjectName("btnMask")
        self.btnSeg = QtWidgets.QPushButton(self.centralwidget)
        self.btnSeg.setGeometry(QtCore.QRect(240, 430, 180, 23))
        self.btnSeg.setObjectName("btnSeg")
        self.btnCalcTraits = QtWidgets.QPushButton(self.centralwidget)
        self.btnCalcTraits.setGeometry(QtCore.QRect(240, 570, 180, 50))
        self.btnCalcTraits.setObjectName("btnCalcTraits")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnBrowse.setText(_translate("MainWindow", "Browse"))
        self.btnLoad.setText(_translate("MainWindow", "Load Image"))
        self.btnMask.setText(_translate("MainWindow", "Mask"))
        self.btnSeg.setText(_translate("MainWindow", "Binaryzation"))
        self.btnCalcTraits.setText(_translate("MainWindow", "Calculate i-Traits"))
import resource_file_rc
