import cv2
import sys
import csv
import numpy as np
from functools import partial
from IR_window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QCheckBox, QListWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from IRProcessing import IR


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.btnSeg.setEnabled(False)
        self.btnMask.setEnabled(False)
        self.btnCalcTraits.setEnabled(False)

        self.btnBrowse.clicked.connect(partial(self.openImage, self.txtImgPth))
        self.btnLoad.clicked.connect(partial(self.loadImage, self.txtImgPth, self.winTemperatureImg))
        self.btnSeg.clicked.connect(partial(self.segmentation, self.winBwImg))
        self.btnMask.clicked.connect(partial(self.temperatureMask, self.winMaskImg))
        self.btnCalcTraits.clicked.connect(self.writeTraits)

        self.temperatureImg = None
        self.bwImg = None
        self.maskImg = None
        self.pseudoImg = None

    def openImage(self, text_edit):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "",
                                                   "Image Files (*.png *.jpg *.bmp *.jpeg *.gif)", options=options)
        if file_path:
            text_edit.setText(file_path)

    def loadImage(self, text_edit, label):
        imagePth = text_edit.text()

        try:
            self.temperatureImg = cv2.imdecode(np.fromfile(imagePth, dtype=np.uint8), 0)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading image: {str(e)}")
            return
        self.pseudoImg = IR.pseudo(self.temperatureImg)
        height, width, channel = self.pseudoImg.shape
        bytesPerLine = 3 * width
        qImg = QPixmap.fromImage(QImage(self.pseudoImg.data, width, height, bytesPerLine, QImage.Format_RGB888))
        label.setPixmap(qImg)
        label.setScaledContents(True)

        self.btnSeg.setEnabled(True)
        self.btnCalcTraits.setEnabled(True)
        self.winBwImg.setPixmap(QPixmap(":/blank.png"))
        self.winMaskImg.setPixmap(QPixmap(":/blank.png"))

    def segmentation(self, label):
        try:
            self.bwImg = IR.equalizeHist(self.temperatureImg)
            self.bwImg = IR.SlidWindow_OTSU(self.bwImg, 50, 50, 10, 10)

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
        self.btnMask.setEnabled(True)

    def temperatureMask(self, label):
        maskImg = self.bwImg
        r, g, b = cv2.split(self.pseudoImg)
        r[maskImg != 255] = 0
        g[maskImg != 255] = 0
        b[maskImg != 255] = 0
        self.maskImg = cv2.merge([r, g, b])
        height, width, channel = self.maskImg.shape
        bytesPerLine = 3 * width
        qImg = QPixmap.fromImage(QImage(self.maskImg.data, width, height, bytesPerLine, QImage.Format_RGB888))
        label.setPixmap(qImg)
        label.setScaledContents(True)

        self.btnMask.setEnabled(False)
        self.btnCalcTraits.setEnabled(True)

    def writeTraits(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        try:
            head = IR.getTraitsHeader()
            traits = IR.calcTraits(self.temperatureImg, self.bwImg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Traits Calculation Failed: {str(e)}")
            return
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
