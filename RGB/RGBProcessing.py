import sys
from typing import Dict, Any

import cv2
import numpy as np
from PIL import Image

from unet import Unet


class Traits:
    @staticmethod
    def getHeader(pipeline: list) -> list:
        Header = []
        for name in pipeline:
            if name == "GLCM":
                temp = ['T' + str(x + 1) for x in range(15)]
            elif name == "HistProperty_L":
                temp = ["M_L", "SE_L", "S_L", "MU3_L", "U_L", "E_L"]
            elif name == "HistProperty_G":
                temp = ["M_G", "SE_G", "S_G", "MU3_G", "U_G", "E_G"]
            elif name == "bwTraits":
                temp = ["TPA", "P", "TBR", "PAR", "FDNIC", "FDIC"]
            elif name == "colorTraits":
                temp = ["GPA", "GPAR"]
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
    def bwTraits(bwImg: np.ndarray):
        # 大田小区的二值图性状计算
        x, y = np.where(bwImg == 255)
        top, bottom = x.min(), x.max()
        left, right = y.min(), y.max()
        bwImg_crop = bwImg[top:bottom + 1, left:right + 1]
        W = right - left + 1
        H = bottom - top + 1
        edge = cv2.Canny(bwImg, 30, 100)
        TPA = bwImg.sum() // 255
        P = edge.sum() // 255
        TBR = TPA / (W * H)
        PAR = P / TPA
        FD = Traits._fractaldim(bwImg)
        FD_crop = Traits._fractaldim(bwImg_crop)

        return [TPA, P, TBR, PAR, FD, FD_crop]

    @staticmethod
    def _fractaldim(bwImg: np.ndarray) -> float:
        area = bwImg.sum() // 255
        if area <= 0:
            return None
        blockSize = 2  # 分块大小
        row, col = bwImg.shape
        arow = int(np.ceil(np.log2(row)))
        acol = int(np.ceil(np.log2(col)))
        loop = arow if arow > acol else acol  # 循环次数，即分块次数
        N = np.zeros([loop + 1], dtype=np.int32)  # 盒子个数
        N[0] = area
        for times in range(1, loop + 1):  # 不同分块大小循环
            arow = (row + blockSize - 1) // blockSize  # 行方向块数
            acol = (col + blockSize - 1) // blockSize  # 列方向块数
            for m in range(arow):
                for n in range(acol):
                    prow_ori = m * blockSize
                    pcol_ori = n * blockSize
                    prow_ter = prow_ori + blockSize if prow_ori + blockSize < row else row
                    pcol_ter = pcol_ori + blockSize if pcol_ori + blockSize < col else col
                    subImg = bwImg[prow_ori:prow_ter, pcol_ori:pcol_ter]
                    if subImg.sum() > 0:
                        N[times] += 1
            blockSize *= 2

        A = B = C = D = 0.0
        xStep = np.log(2)
        for i in range(loop + 1):
            xi = i * xStep
            A += xi * xi
            B += xi
            yi = np.log(N[i])
            C += xi * yi
            D += yi
        FD = -(C * (loop + 1) - B * D) / (A * (loop + 1) - B * B)
        return FD

    @staticmethod
    def EGThreshold(rgbImg: np.ndarray, bwImg: np.ndarray, EGthre=0.05, RGBthre=30):
        TPA = (bwImg // 255).sum()
        b = rgbImg[:, :, 0].astype(np.float64)
        g = rgbImg[:, :, 1].astype(np.float64)
        r = rgbImg[:, :, 2].astype(np.float64)
        rgb = r + g + b
        eg = g / rgb * 2 - r / rgb - b / rgb
        bwImg[eg <= EGthre] = 0
        bwImg[rgb <= RGBthre] = 0
        GPA = (bwImg // 255).sum()
        GPAR = GPA / TPA
        return [GPA, GPAR]


class RGB:
    unet = Unet()
    @staticmethod
    def _devide_img_uNet(img, size):
        h, w, _ = img.shape
        top = (size - h % size) // 2
        bottom = (size - h % size) - top
        left = (size - w % size) // 2
        right = (size - w % size) - left
        # print("h:{} w:{} top:{} bottom:{} left:{} right:{}".format(h,w,top,bottom,left,right))
        img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        #   将图像大小padding成size的倍数
        h_pad, w_pad, _ = img.shape

        h_win = size
        w_win = size
        stride_h = 250
        stride_w = 250
        top_list = [x for x in range(0, h_pad // 2, stride_h)] + list(
            reversed([x for x in range(h_pad - h_win, h_pad // 2 - stride_h, -stride_h)]))
        left_list = [x for x in range(0, w_pad // 2, stride_w)] + list(
            reversed([x for x in range(w_pad - w_win, w_pad // 2 - stride_w, -stride_w)]))
        num = 0

        classes: Dict[Any, np.ndarray] = {}  # 创建一个{类别:矩阵}的字典, 用于存放被识别次数
        for i in range(len(top_list)):
            for j in range(len(left_list)):
                num += 1
                crop_img = img[top_list[i]:top_list[i] + h_win, left_list[j]:left_list[j] + w_win, :]
                crop_img_PIL = Image.fromarray(cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB))
                seg_img_PIL = RGB.unet.detect_image(crop_img_PIL)
                seg_img = np.array(seg_img_PIL)[:, :, 0]
                sub_classes = np.unique(seg_img)

                for cls in sub_classes:

                    if cls not in classes.keys():
                        #   如果不存在该类别, 则进行初始化
                        classes[cls] = np.zeros(shape=(h_pad, w_pad))

                    classes[cls][top_list[i]:top_list[i] + h_win, left_list[j]:left_list[j] + w_win][
                        seg_img == cls] += 1

        seg_img = np.zeros(shape=(h_pad, w_pad), dtype=np.uint8)  # 最终生成的分割图像
        for row in range(h_pad):
            for col in range(w_pad):
                decision = np.array([classes[x][row, col] for x in classes.keys()])
                seg_img[row, col] = list(classes.keys())[np.argmax(decision)]

        x0 = left
        x1 = w_pad - right
        y0 = top
        y1 = h_pad - bottom

        seg_img_crop = seg_img[y0:y1, x0:x1]
        return seg_img_crop

    @staticmethod
    def getSegImg(img: np.ndarray) -> np.ndarray:
        size = 512
        return RGB._devide_img_uNet(img, size)

    @staticmethod
    def calcTraits(rgbImg: np.ndarray, bwImg: np.ndarray):
        bwTraits = Traits.bwTraits(bwImg)
        colorTraits = Traits.EGThreshold(rgbImg, bwImg)
        g_img = rgbImg[:, :, 1]
        l_img = cv2.cvtColor(rgbImg, cv2.COLOR_BGR2HLS)[:, :, 1]
        white = np.ones_like(g_img) * 255
        HistProperty_G = Traits.HistProperty(g_img, white)
        HistProperty_L = Traits.HistProperty(l_img, white)
        GLCM_G = Traits.GLCM(g_img, bwImg)

        return bwTraits + colorTraits + HistProperty_G + HistProperty_L + GLCM_G

    @staticmethod
    def getTraitsHeader(pipeline=["bwTraits", "colorTraits", "HistProperty_G", "HistProperty_L", "GLCM"]):
        return Traits.getHeader(pipeline)
