# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Root_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 650)
        MainWindow.setMaximumSize(QtCore.QSize(400, 650))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.winRgbImg = QtWidgets.QLabel(self.centralwidget)
        self.winRgbImg.setGeometry(QtCore.QRect(20, 20, 180, 300))
        self.winRgbImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winRgbImg.setText("")
        self.winRgbImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winRgbImg.setScaledContents(True)
        self.winRgbImg.setObjectName("winRgbImg")
        self.winBwImg = QtWidgets.QLabel(self.centralwidget)
        self.winBwImg.setGeometry(QtCore.QRect(200, 320, 180, 300))
        self.winBwImg.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.winBwImg.setText("")
        self.winBwImg.setPixmap(QtGui.QPixmap(":/blank.png"))
        self.winBwImg.setScaledContents(True)
        self.winBwImg.setObjectName("winBwImg")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 20, 180, 300))
        self.label.setMinimumSize(QtCore.QSize(180, 300))
        self.label.setMaximumSize(QtCore.QSize(180, 300))
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/segformer.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.btnLoad = QtWidgets.QPushButton(self.centralwidget)
        self.btnLoad.setGeometry(QtCore.QRect(115, 360, 75, 23))
        self.btnLoad.setObjectName("btnLoad")
        self.btnBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.btnBrowse.setGeometry(QtCore.QRect(30, 360, 75, 23))
        self.btnBrowse.setObjectName("btnBrowse")
        self.txtImgPth = QtWidgets.QLineEdit(self.centralwidget)
        self.txtImgPth.setGeometry(QtCore.QRect(30, 330, 160, 20))
        self.txtImgPth.setObjectName("txtImgPth")
        self.btnSeg = QtWidgets.QPushButton(self.centralwidget)
        self.btnSeg.setGeometry(QtCore.QRect(30, 450, 160, 23))
        self.btnSeg.setObjectName("btnSeg")
        self.btnCalcTraits = QtWidgets.QPushButton(self.centralwidget)
        self.btnCalcTraits.setGeometry(QtCore.QRect(30, 570, 160, 50))
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
        self.btnLoad.setText(_translate("MainWindow", "Load Image"))
        self.btnBrowse.setText(_translate("MainWindow", "Browse"))
        self.btnSeg.setText(_translate("MainWindow", "Segmentation"))
        self.btnCalcTraits.setText(_translate("MainWindow", "Calculate i-Traits"))
import resource_file_rc
