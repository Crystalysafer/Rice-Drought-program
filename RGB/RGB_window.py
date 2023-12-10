# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RGB_window.ui'
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
        self.winRgbImg = QtWidgets.QLabel(self.centralwidget)
        self.winRgbImg.setGeometry(QtCore.QRect(25, 25, 200, 200))
        self.winRgbImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winRgbImg.setText("")
        self.winRgbImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winRgbImg.setScaledContents(True)
        self.winRgbImg.setObjectName("winRgbImg")
        self.winBwImg = QtWidgets.QLabel(self.centralwidget)
        self.winBwImg.setGeometry(QtCore.QRect(225, 225, 200, 200))
        self.winBwImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winBwImg.setText("")
        self.winBwImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winBwImg.setScaledContents(True)
        self.winBwImg.setObjectName("winBwImg")
        self.winMaskImg = QtWidgets.QLabel(self.centralwidget)
        self.winMaskImg.setGeometry(QtCore.QRect(25, 425, 200, 200))
        self.winMaskImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winMaskImg.setText("")
        self.winMaskImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winMaskImg.setScaledContents(True)
        self.winMaskImg.setObjectName("winMaskImg")
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
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(240, 55, 75, 23))
        self.btnBrowse.setObjectName("btnBrowse")
        self.txtImgPth = QtWidgets.QLineEdit(self.centralwidget)
        self.txtImgPth.setGeometry(QtCore.QRect(240, 30, 180, 20))
        self.txtImgPth.setObjectName("txtImgPth")
        self.btnLoad = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoad.setGeometry(QtCore.QRect(345, 55, 75, 23))
        self.btnLoad.setObjectName("btnLoad")
        self.btnSeg = QtWidgets.QPushButton(self.centralwidget)
        self.btnSeg.setGeometry(QtCore.QRect(240, 430, 180, 23))
        self.btnSeg.setObjectName("btnSeg")
        self.btnCalcTraits = QtWidgets.QPushButton(self.centralwidget)
        self.btnCalcTraits.setGeometry(QtCore.QRect(240, 570, 180, 50))
        self.btnCalcTraits.setObjectName("btnCalcTraits")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setEnabled(True)
        self.label_5.setGeometry(QtCore.QRect(220, 70, 200, 160))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap(":/UNet.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnMask.setText(_translate("MainWindow", "Mask"))
        self.btnBrowse.setText(_translate("MainWindow", "Browse"))
        self.btnLoad.setText(_translate("MainWindow", "Load Image"))
        self.btnSeg.setText(_translate("MainWindow", "Segmentation"))
        self.btnCalcTraits.setText(_translate("MainWindow", "Calculate i-Traits"))
import resource_file_rc
