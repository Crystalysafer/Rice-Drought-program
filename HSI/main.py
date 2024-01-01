import cv2
import sys
import csv
import numpy as np
from functools import partial
from HSI_window import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QCheckBox, QListWidgetItem
from PyQt5.QtGui import QPixmap, QImage
from HSIProcessing import HSI



class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.btnSeg.setEnabled(False)
        self.btnExtraction.setEnabled(False)
        self.spinBoxBand.setEnabled(False)
        self.btnMask.setEnabled(False)
        self.btnCalcTraits.setEnabled(False)

        self.btnBrowse.clicked.connect(partial(self.openSpectral, self.txtImgPth))
        self.btnLoad.clicked.connect(partial(self.loadSpectral, self.txtImgPth, self.labelLoad))
        self.btnExtraction.clicked.connect(partial(self.extractionSpectral, self.winGrayImg))
        self.btnSeg.clicked.connect(partial(self.segmentation, self.winBwImg))
        self.btnMask.clicked.connect(partial(self.spectralMask, self.winMaskImg))
        self.btnCalcTraits.clicked.connect(self.writeTraits)

        self.spectral = None
        self.grayImg = None
        self.bwImg = None
        self.maskImg = None

    def openSpectral(self, text_edit):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Spectral File", "",
                                                   "Spectral Files (*.npy)", options=options)
        if file_path:
            text_edit.setText(file_path)

    def loadSpectral(self, text_edit, label):
        spectralPth = text_edit.text()
        try:
            self.spectral = np.load(spectralPth)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error loading spctral: {str(e)}")
            return

        label.setText("Spectral Data Loaded")
        label.setStyleSheet("color: red;")

        self.btnExtraction.setEnabled(True)
        self.spinBoxBand.setEnabled(True)
        self.btnCalcTraits.setEnabled(False)
        self.winBwImg.setPixmap(QPixmap(":/blank.png"))
        self.winMaskImg.setPixmap(QPixmap(":/blank.png"))

    def extractionSpectral(self, label):
        self.btnSeg.setEnabled(True)
        bandIndex = self.spinBoxBand.value() - 1
        self.grayImg = self.spectral[:, :, bandIndex]
        self.grayImg = cv2.normalize(self.grayImg, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX).astype('uint8')
        grayImg_3 = cv2.merge([self.grayImg, self.grayImg, self.grayImg])
        height, width, channel = grayImg_3.shape
        bytesPerLine = 3 * width
        qImg = QPixmap.fromImage(QImage(grayImg_3.data, width, height, bytesPerLine, QImage.Format_RGB888))
        label.setPixmap(qImg)
        label.setScaledContents(True)

        self.winBwImg.setPixmap(QPixmap(":/blank.png"))
        self.winMaskImg.setPixmap(QPixmap(":/blank.png"))

    def segmentation(self, label):
        def _removesmall(img, area=None):
            _, labels, stats, _ = cv2.connectedComponentsWithStats(img, connectivity=8)
            a_array = stats[:, 4].reshape(-1)
            a_mean = np.mean(np.sort(a_array)[:-1])
            if area is None:
                area = a_mean
            for index, a in enumerate(a_array):
                if a < area:
                    img[labels == index] = 0
            return img

        def _remove_overexposure(srcImg, thre=0.99) -> np.ndarray:
            #   去除白色离群值
            flat_sort = srcImg.flatten()
            flat_sort.sort()
            thre_idx = int(thre * len(flat_sort))
            thre_val = flat_sort[thre_idx]
            srcImg[srcImg > thre_val] = 0

            return srcImg

        self.bwImg = _remove_overexposure(self.grayImg)
        _, self.bwImg = cv2.threshold(self.bwImg, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        self.bwImg = _removesmall(self.bwImg, 20)

        bwImg_3 = cv2.merge([self.bwImg, self.bwImg, self.bwImg])
        height, width, channel = bwImg_3.shape
        bytesPerLine = 3 * width
        qImg = QPixmap.fromImage(QImage(bwImg_3.data, width, height, bytesPerLine, QImage.Format_RGB888))
        label.setPixmap(qImg)
        label.setScaledContents(True)

        self.btnSeg.setEnabled(False)
        self.btnMask.setEnabled(True)

        self.winMaskImg.setPixmap(QPixmap(":/blank.png"))

    def spectralMask(self, label):
        maskImg = self.bwImg
        grayscale = self.grayImg
        grayscale[maskImg != 255] = 0
        self.maskImg = cv2.merge([grayscale, grayscale, grayscale])
        height, width, channel = self.maskImg.shape
        bytesPerLine = 3 * width
        qImg = QPixmap.fromImage(QImage(self.maskImg.data, width, height, bytesPerLine, QImage.Format_RGB888))
        label.setPixmap(qImg)
        label.setScaledContents(True)

        self.btnMask.setEnabled(False)
        self.btnSeg.setEnabled(False)
        self.btnCalcTraits.setEnabled(True)

    def writeTraits(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        try:
            head = HSI.getSpectralTraitsHeader()
            traits = HSI.getSpectralTraits(self.spectral, self.bwImg)
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
