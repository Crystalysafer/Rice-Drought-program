import os
import cv2
import numpy as np
from typing import Dict, Union, Any
import matplotlib.pyplot as plt


class Traits:
    @staticmethod
    def getHeader(pipeline: list) -> list:
        Header = []
        for name in pipeline:
            if name == "GLCM":
                temp = ['T' + str(x + 1) for x in range(15)]
            elif name == "HistProperty":
                temp = ["M_Hist", "SE_Hist", "S_Hist", "MU3_Hist", "U_Hist", "E_Hist"]
            elif name == "TemperatureTraits":
                temp = ["Max", "Min", "Mean", "Quarter", "Meadian", "Three-quarter"]
            Header += temp
        return Header

    @staticmethod
    def GLCM(img_gray: np.ndarray, img_mask: np.ndarray, ngrad=16, ngray=16) -> list:
        """Gray Level-Gradient Co-occurrence Matrix,取归一化后的灰度值、梯度值分别为16、16"""
        # 利用sobel算子分别计算x-y方向上的梯度值
        img_gray = img_gray * (img_mask // 255)
        kernel = np.array([[-1, -1, -1],
                           [-1, 8, -1],
                           [-1, -1, -1]])
        grad = cv2.filter2D(img_gray, -1, kernel)  # 计算梯度值
        height, width = img_gray.shape
        grad = np.asarray(1.0 * grad * (ngrad - 1) / grad.max(), dtype=np.int16)
        gray = np.asarray(1.0 * img_gray * (ngray - 1) / img_gray.max(), dtype=np.int16)  # 0-255变换为0-15
        gray_grad = np.zeros([ngray, ngrad])  # 灰度梯度共生矩阵
        N = 0
        for i in range(height):
            for j in range(width):
                if img_mask[i][j] != 0:
                    N += 1
                    gray_value = gray[i][j]
                    grad_value = grad[i][j]
                    gray_grad[gray_value][grad_value] += 1
        gray_grad = 1.0 * gray_grad / N  # 归一化灰度梯度矩阵，减少计算量
        glgcm_features = Traits._get_glgcm_features(gray_grad).tolist()
        return glgcm_features

    @staticmethod
    def _get_glgcm_features(mat):
        """根据灰度梯度共生矩阵计算纹理特征量，包括相关性、小梯度优势、大梯度优势、能量、灰度分布不均匀性、梯度分布不均匀性、
        灰度均值、梯度均值、灰度熵、梯度熵、混合熵、差分矩、逆差分矩、灰度标准差、梯度标准差"""
        sum_mat = mat.sum()
        small_grads_dominance = big_grads_dominance = gray_asymmetry = grads_asymmetry = energy = gray_mean = grads_mean = 0.0
        gray_variance = grads_variance = corelation = gray_entropy = grads_entropy = entropy = inertia = differ_moment = 0.0
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                small_grads_dominance += mat[i][j] / ((j + 1) ** 2)
                big_grads_dominance += mat[i][j] * (j + 1) ** 2
                energy += mat[i][j] ** 2
                if mat[i].sum() != 0:
                    gray_entropy -= mat[i][j] * np.log(mat[i].sum())
                if mat[:, j].sum() != 0:
                    grads_entropy -= mat[i][j] * np.log(mat[:, j].sum())
                if mat[i][j] != 0:
                    entropy -= mat[i][j] * np.log(mat[i][j])
                    inertia += (i - j) ** 2 * mat[i][j]
                differ_moment += mat[i][j] / (1 + (i - j) ** 2)

            gray_asymmetry += mat[i].sum() ** 2
            gray_mean += (i + 1) * mat[i].sum()
        for j in range(mat.shape[1]):
            grads_asymmetry += mat[:, j].sum() ** 2
            grads_mean += (j + 1) * mat[:, j].sum()
        for i in range(mat.shape[0]):
            gray_variance_temp = 0
            for j in range(mat.shape[1]):
                gray_variance_temp += mat[i][j]
            gray_variance += (i - gray_mean) ** 2 * gray_variance_temp
        for j in range(mat.shape[1]):
            grads_variance_temp = 0
            for i in range(mat.shape[0]):
                grads_variance_temp += mat[i][j]
            grads_variance += (j - grads_mean) ** 2 * grads_variance_temp
        small_grads_dominance /= sum_mat
        big_grads_dominance /= sum_mat
        gray_asymmetry /= sum_mat
        grads_asymmetry /= sum_mat
        gray_variance = gray_variance ** 0.5
        grads_variance = grads_variance ** 0.5
        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                corelation += (i - gray_mean) * (j - grads_mean) * mat[i][j]
        corelation = corelation / gray_mean / grads_mean
        glgcm_features = [corelation, small_grads_dominance, big_grads_dominance, energy, gray_asymmetry,
                          grads_asymmetry,
                          gray_mean, grads_mean,
                          gray_entropy, grads_entropy, entropy, inertia, differ_moment, gray_variance, grads_variance]
        return np.round(glgcm_features, 4)

    @staticmethod
    def HistProperty(img_gray: np.ndarray, img_mask: np.ndarray, bins=32) -> list:

        m = sigma = R = mu3 = U = entropy = 0.0
        N = 0
        interval = 256 // bins
        img_gray = img_gray // interval
        hist = np.zeros([bins], dtype=np.int32)
        # p = np.zeros([bins], dtype=np.float64)

        height, width = img_gray.shape
        for i in range(height):
            for j in range(width):
                if img_mask[i][j] != 0:
                    N += 1
                    hist[img_gray[i][j]] += 1
        p = hist / N
        m = (p * list(range(bins))).sum()
        for i in range(bins):
            sigma += (i - m) ** 2 * p[i]
            mu3 += (i - m) ** 3 * p[i]
            U += p[i] ** 2
            if p[i] != 0:
                entropy += (-p[i]) * np.log(p[i]) / np.log(2)
        sigma = sigma ** 0.5
        R = 1 - 1 / (1 + sigma)

        return [m, sigma, R, mu3, U, entropy]

    @staticmethod
    def TemperatureTraits(img_gray: np.ndarray, img_mask: np.ndarray) -> list:
        img_gray = img_gray * (img_mask // 255)
        img_gray = img_gray.flatten()[img_gray.flatten() != 0]
        img_gray = (img_gray / 4).astype(np.float32)

        # 计算最大值、最小值和均值
        max_value = np.max(img_gray)
        min_value = np.min(img_gray)
        mean_value = np.mean(img_gray)

        # 计算四分位数、中位数和四分之三位数
        quarter = np.percentile(img_gray, 25)
        median = np.median(img_gray)
        three_quarter = np.percentile(img_gray, 75)

        return [max_value, min_value, mean_value, quarter, median, three_quarter]


class IR:
    @staticmethod
    def SlidWindow_OTSU(srcImg: np.ndarray,
                        win_h: int, win_w: int,
                        stride_h: int, stride_w: int) -> np.ndarray:
        if len(srcImg.shape) == 3:
            srcImg = srcImg[:, :, 0]
        h, w = srcImg.shape

        if (h < win_h) or (w < win_h) or (win_h < 0) or (win_w < 0):
            print("Wrong win size!")
            return None

        top = (h % win_h) // 2
        bottom = h - (h % win_h) + top
        left = (w % win_w) // 2
        right = w - (w % win_w) + left

        img_crop = srcImg[top:bottom, left:right]
        h_crop, w_crop = img_crop.shape

        top_list = [x + top for x in range(0, h_crop // 2, stride_h)] + list(
            reversed([x + top for x in range(h_crop - win_h, h_crop // 2 - stride_h, -stride_h)]))
        left_list = [x + left for x in range(0, w_crop // 2, stride_w)] + list(
            reversed([x + left for x in range(w_crop - win_w, w_crop // 2 - stride_w, -stride_w)]))
        top_list.insert(0, 0)
        top_list.append(h - win_h)
        left_list.insert(0, 0)
        left_list.append(w - win_w)
        classes: Dict[Any, np.ndarray] = {}  # 创建一个{类别:矩阵}的字典, 用于存放被识别次数

        for i in range(len(top_list)):
            for j in range(len(left_list)):
                crop_img = srcImg[top_list[i]:top_list[i] + win_h, left_list[j]:left_list[j] + win_w]
                # _, seg_img = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                _, seg_img = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                sub_classes = np.unique(seg_img)
                for cls in sub_classes:

                    if cls not in classes.keys():
                        #   如果不存在该类别, 则进行初始化
                        classes[cls] = np.zeros(shape=(h, w))

                    classes[cls][top_list[i]:top_list[i] + win_h, left_list[j]:left_list[j] + win_w][seg_img == cls] += 1

        seg_img = np.zeros(shape=(h, w), dtype=np.uint8)  # 最终生成的分割图像
        for row in range(h):
            for col in range(w):
                decision = np.array([classes[x][row, col] for x in classes.keys()])
                seg_img[row, col] = list(classes.keys())[np.argmax(decision)]

        return seg_img

    @staticmethod
    def equalizeHist(grayImg):
        return cv2.equalizeHist(grayImg)

    @staticmethod
    def pseudo(temperatureImg):
        vmin = temperatureImg.min()
        vmax = temperatureImg.max()
        gray_image = ((temperatureImg - vmin) / (vmax - vmin) * 300 + 150).astype("int")
        cmap = plt.get_cmap('hsv_r')
        pseudo_color_image = cmap(gray_image)
        return (pseudo_color_image[:, :, :3]*255).astype(np.uint8)

    @staticmethod
    def calcTraits(temperatureImg, maskImg=None):
        if maskImg is None:
            maskImg = np.ones_like(temperatureImg, dtype=np.uint8) * 255

        HistProperty = Traits.HistProperty(temperatureImg, maskImg)
        GLCM = Traits.GLCM(temperatureImg, maskImg)
        TemperatureTraits = Traits.TemperatureTraits(temperatureImg, maskImg)
        return HistProperty + GLCM + TemperatureTraits

    @staticmethod
    def getTraitsHeader(pipeline=["HistProperty", "GLCM", "TemperatureTraits"]):
        return Traits.getHeader(pipeline)
