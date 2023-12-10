# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HSI_window.ui'
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
        self.winGrayImg = QtWidgets.QLabel(self.centralwidget)
        self.winGrayImg.setGeometry(QtCore.QRect(25, 25, 200, 200))
        self.winGrayImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winGrayImg.setText("")
        self.winGrayImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winGrayImg.setScaledContents(True)
        self.winGrayImg.setObjectName("winGrayImg")
        self.winMaskImg = QtWidgets.QLabel(self.centralwidget)
        self.winMaskImg.setGeometry(QtCore.QRect(25, 425, 200, 200))
        self.winMaskImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winMaskImg.setText("")
        self.winMaskImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winMaskImg.setScaledContents(True)
        self.winMaskImg.setObjectName("winMaskImg")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(240, 80, 75, 23))
        self.btnBrowse.setObjectName("btnBrowse")
        self.txtImgPth = QtWidgets.QLineEdit(self.centralwidget)
        self.txtImgPth.setGeometry(QtCore.QRect(240, 55, 180, 20))
        self.txtImgPth.setObjectName("txtImgPth")
        self.btnLoad = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoad.setGeometry(QtCore.QRect(345, 80, 75, 23))
        self.btnLoad.setObjectName("btnLoad")
        self.labelLoad = QtWidgets.QLabel(self.centralwidget)
        self.labelLoad.setGeometry(QtCore.QRect(250, 30, 161, 16))
        self.labelLoad.setObjectName("labelLoad")
        self.spinBoxBand = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxBand.setGeometry(QtCore.QRect(360, 160, 45, 26))
        self.spinBoxBand.setMinimum(1)
        self.spinBoxBand.setMaximum(224)
        self.spinBoxBand.setObjectName("spinBoxBand")
        self.btnExtraction = QtWidgets.QPushButton(self.centralwidget)
        self.btnExtraction.setGeometry(QtCore.QRect(240, 140, 111, 51))
        self.btnExtraction.setObjectName("btnExtraction")
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
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(360, 140, 31, 20))
        self.label_2.setObjectName("label_2")
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
        self.btnLoad.setText(_translate("MainWindow", "Load Data"))
        self.labelLoad.setText(_translate("MainWindow", "Please Load Spectral Data"))
        self.btnExtraction.setText(_translate("MainWindow", "Spectral Image\n"
"Extraction"))
        self.btnMask.setText(_translate("MainWindow", "Mask"))
        self.btnSeg.setText(_translate("MainWindow", "Binaryzation"))
        self.btnCalcTraits.setText(_translate("MainWindow", "Calculate i-Traits"))
        self.label_2.setText(_translate("MainWindow", "Band"))
import resource_file_rc
