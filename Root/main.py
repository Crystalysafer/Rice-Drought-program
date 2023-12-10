import cv2
import sys
import csv
import numpy as np
import paddle
from functools import partial
from Root_window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import  RootProcessing


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.btnSeg.setEnabled(False)
        self.btnCalcTraits.setEnabled(False)

        self.btnBrowse.clicked.connect(partial(self.openImage, self.txtImgPth))
        self.btnLoad.clicked.connect(partial(self.loadImage, self.txtImgPth, self.winRgbImg))
        self.btnSeg.clicked.connect(partial(self.segmentation, self.winBwImg))
        self.btnCalcTraits.clicked.connect(self.writeTraits)

        self.rgbImg = None
        self.bwImg = None

    def openImage(self, text_edit):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.bmp *.jpeg *.gif)", options=options)
        if file_path:
            text_edit.setText(file_path)

    def loadImage(self, text_edit, label):
        imagePth = text_edit.text()
        label.setPixmap(QPixmap(imagePth))
        label.setScaledContents(True)
        try:
            self.rgbImg = cv2.imdecode(np.fromfile(imagePth, dtype=np.uint8), cv2.IMREAD_COLOR)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading image: {str(e)}")
            return

        self.btnSeg.setEnabled(True)
        self.winBwImg.setPixmap(QPixmap(":/blank.png"))
        self.btnCalcTraits.setEnabled(False)

    def segmentation(self, label):
        try:
            self.bwImg = RootProcessing.getSegImg(self.rgbImg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Image Segmentation Failed: {str(e)}")
            return
        bwImg_rgb = cv2.cvtColor(self.bwImg, cv2.COLOR_GRAY2RGB)
        height, width, channel = bwImg_rgb.shape
        bytesPerLine = 3 * width
        qImg = QPixmap.fromImage(QImage(bwImg_rgb.data, width, height, bytesPerLine, QImage.Format_RGB888))
        label.setPixmap(qImg)
        label.setScaledContents(True)

        self.btnSeg.setEnabled(False)
        self.btnCalcTraits.setEnabled(True)

    def writeTraits(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        try:
            traits = RootProcessing.calcTraits(self.bwImg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Traits Calculation Failed: {str(e)}")
            return
        head = RootProcessing.getHeader()

        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(head)
                writer.writerow(traits)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Traits Writing Failed: {str(e)}")
            return

        self.btnCalcTraits.setEnabled(False)
        QMessageBox.information(self, "Completion", "Completion!")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
