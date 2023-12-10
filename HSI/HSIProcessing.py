import numpy as np
import cv2


class HSI:
    @staticmethod
    def getSpectralTraitsHeader(bands_num=224, CommonSpectralIndex=True) -> list:
        #   [Area, A, dA, ddA, log10(A)]
        A = ['A' + str(x + 1) for x in range(bands_num)]
        dA = ['dA' + str(x + 1) for x in range(1, bands_num - 1)]
        ddA = ['ddA' + str(x + 1) for x in range(2, bands_num - 2)]
        lgA = ['lgA' + str(x + 1) for x in range(bands_num)]
        header = A + dA + ddA + lgA

        if CommonSpectralIndex:
            CommonSpectralIndex_NameList = [
                'NDVI', 'SR', 'EVI', 'ARVI', 'SG',
                'NDVI705', 'mSR705', 'mNDVI705', 'VOG1', 'VOG2', 'VOG3', 'REP',
                'PRI', 'SIPI', 'RG',
                'CRI1', 'CRI2', 'ARI1', 'ARI2',
                'WBI'
            ]
            header = header + CommonSpectralIndex_NameList

        return header

    @staticmethod
    def _dx_2nd_Order_Central(x: np.ndarray) -> np.ndarray:
        #   二阶中心求导
        x_dec = x[:, :-2]  # X_i-1
        x_inc = x[:, 2:]  # X_i+1
        dx = (x_inc - x_dec) / 2
        return dx

    @staticmethod
    def CommonSpectralIndex(x: np.ndarray, minBand=400, maxBand=1000, bands_num=224) -> np.ndarray:
        #   常见光谱指数
        NIR = 800
        RED = 680
        BLUE = 450

        def _Band2Index(band, minBand=minBand, maxBand=maxBand, bands_num=bands_num) -> int:
            #   输入400~1000nm波长, 返回对应的索引
            if band < minBand or band > maxBand:
                return -1
            return int((band - minBand) / ((maxBand - minBand) / bands_num))

        def _Index2Band(index, minBand=minBand, maxBand=maxBand, bands_num=bands_num) -> float:
            #   输入索引, 返回对应的波长
            if index < 0 or index > bands_num - 1:
                return -1
            return index * ((maxBand - minBand) / bands_num) + minBand

        def _NormalizedDifference(spectralData: np.ndarray, band1, band2) -> np.ndarray:
            #   归一化差值
            R1 = spectralData[:, _Band2Index(band1)]
            R2 = spectralData[:, _Band2Index(band2)]
            return (R1 - R2) / (R1 + R2)

        def _Ratio(spectralData: np.ndarray, band1, band2) -> np.ndarray:
            #   获取两波段比值
            R1 = spectralData[:, _Band2Index(band1)]
            R2 = spectralData[:, _Band2Index(band2)]
            return R1 / R2

        def NDVI(x: np.ndarray) -> np.ndarray:
            #   归一化差值植被指数
            return np.expand_dims(_NormalizedDifference(x, NIR, RED), axis=1)

        def SR(x: np.ndarray) -> np.ndarray:
            #   简化比值植被指数
            return np.expand_dims(_Ratio(x, NIR, RED), axis=1)

        def EVI(x: np.ndarray) -> np.ndarray:
            #   增强型植被指数
            R_NIR = x[:, _Band2Index(NIR)]
            R_RED = x[:, _Band2Index(RED)]
            R_BLUE = x[:, _Band2Index(BLUE)]

            numerator = R_NIR - R_RED
            denominator = R_NIR + 6 * R_RED - 7.5 * R_BLUE + 1
            return np.expand_dims(2.5 * numerator / denominator, axis=1)

        def ARVI(x: np.ndarray) -> np.ndarray:
            #   大气阻抗植被指数
            R_NIR = x[:, _Band2Index(NIR)]
            R_RED = x[:, _Band2Index(RED)]
            R_BLUE = x[:, _Band2Index(BLUE)]

            numerator = R_NIR - (2 * R_RED - R_BLUE)
            denominator = R_NIR + (2 * R_RED - R_BLUE)
            return np.expand_dims(numerator / denominator, axis=1)

        def SG(x: np.ndarray) -> np.ndarray:
            #   绿波段总和指数
            headIndex = _Band2Index(500)
            tailIndex = _Band2Index(600)

            return np.expand_dims(np.mean(x[:, headIndex:tailIndex + 1], axis=1), axis=1)

        def NDVI_705(x: np.ndarray) -> np.ndarray:
            #   红边归一化差值植被指数
            return np.expand_dims(_NormalizedDifference(x, 750, 705), axis=1)

        def mSR_705(x: np.ndarray) -> np.ndarray:
            #   改进型红边比值植被指数
            R_750 = x[:, _Band2Index(750)]
            R_445 = x[:, _Band2Index(445)]
            R_705 = x[:, _Band2Index(705)]

            numerator = R_750 - R_445
            denominator = R_705 - R_445

            return np.expand_dims(numerator / denominator, axis=1)

        def mNDVI_705(x: np.ndarray) -> np.ndarray:
            #   改进型红边归一化差值植被指数
            R_750 = x[:, _Band2Index(750)]
            R_445 = x[:, _Band2Index(445)]
            R_705 = x[:, _Band2Index(705)]

            numerator = R_750 - R_705
            denominator = R_750 + R_705 - 2 * R_445

            return np.expand_dims(numerator / denominator, axis=1)

        def VOG1(x: np.ndarray) -> np.ndarray:
            #   Vogelmann红边指数1
            return np.expand_dims(_Ratio(x, 740, 720), axis=1)

        def VOG2(x: np.ndarray) -> np.ndarray:
            #   Vogelmann红边指数2
            R_734 = x[:, _Band2Index(734)]
            R_747 = x[:, _Band2Index(747)]
            R_715 = x[:, _Band2Index(715)]
            R_726 = x[:, _Band2Index(726)]

            numerator = R_734 - R_747
            denominator = R_715 + R_726

            return np.expand_dims(numerator / denominator, axis=1)

        def VOG3(x: np.ndarray) -> np.ndarray:
            #   Vogelmann红边指数3
            R_734 = x[:, _Band2Index(734)]
            R_747 = x[:, _Band2Index(747)]
            R_715 = x[:, _Band2Index(715)]
            R_720 = x[:, _Band2Index(720)]

            numerator = R_734 - R_747
            denominator = R_715 + R_720

            return np.expand_dims(numerator / denominator, axis=1)

        def REP(x: np.ndarray) -> np.ndarray:
            #   红边位置指数
            headIndex = _Band2Index(680)
            tailIndex = _Band2Index(760)
            x = x[:, headIndex:tailIndex + 1]
            dx = HSI._dx_2nd_Order_Central(x)
            maxDx_index = np.argmax(dx, axis=1) + headIndex
            maxDx_band = np.array(list(map(_Index2Band, maxDx_index)))
            return np.expand_dims(maxDx_band, axis=1)

        def PRI(x: np.ndarray) -> np.ndarray:
            #   光化学反射指数
            return np.expand_dims(_NormalizedDifference(x, 570, 531), axis=1)

        def SIPI(x: np.ndarray) -> np.ndarray:
            #   结构不敏感色素指数
            return np.expand_dims(_NormalizedDifference(x, 800, 445), axis=1)

        def RG(x: np.ndarray) -> np.ndarray:
            #   红绿比值指数
            #   绿色波段500-580nm, 红色波段600-680nm
            return np.expand_dims(
                np.mean(x[:, _Band2Index(600):_Band2Index(680)], axis=1) / np.mean(
                    x[:, _Band2Index(500):_Band2Index(580)],
                    axis=1), axis=1)

        def CRI1(x: np.ndarray) -> np.ndarray:
            #   类胡萝卜素反射指数1
            R_510 = x[:, _Band2Index(510)]
            R_550 = x[:, _Band2Index(550)]

            return np.expand_dims(1 / R_510 - 1 / R_550, axis=1)

        def CRI2(x: np.ndarray) -> np.ndarray:
            #   类胡萝卜素反射指数2
            R_510 = x[:, _Band2Index(510)]
            R_700 = x[:, _Band2Index(700)]

            return np.expand_dims(1 / R_510 - 1 / R_700, axis=1)

        def ARI1(x: np.ndarray) -> np.ndarray:
            #   花青素反射指数1
            R_550 = x[:, _Band2Index(550)]
            R_700 = x[:, _Band2Index(700)]

            return np.expand_dims(1 / R_550 - 1 / R_700, axis=1)

        def ARI2(x: np.ndarray) -> np.ndarray:
            #   花青素反射指数2
            R_550 = x[:, _Band2Index(550)]
            R_700 = x[:, _Band2Index(700)]
            R_800 = x[:, _Band2Index(800)]

            return np.expand_dims(R_800 * (1 / R_550 - 1 / R_700), axis=1)

        def WBI(x: np.ndarray) -> np.ndarray:
            #   水波段指数
            return np.expand_dims(_Ratio(x, 900, 970), axis=1)

        CommonSpectralIndex = np.concatenate((
            NDVI(x), SR(x), EVI(x), ARVI(x), SG(x),
            NDVI_705(x), mSR_705(x), mNDVI_705(x), VOG1(x), VOG2(x), VOG3(x), REP(x),
            PRI(x), SIPI(x), RG(x),
            CRI1(x), CRI2(x), ARI1(x), ARI2(x),
            WBI(x)
        ), axis=1)

        return CommonSpectralIndex

    @staticmethod
    def getSpectralTraits(spectraldata, maskImg):
        maskSpectral = cv2.add(spectraldata, np.zeros_like(spectraldata, dtype=np.float32), mask=maskImg)
        spectralData_T = np.sum(np.sum(maskSpectral, 0), 0)
        spectralData_T = spectralData_T.reshape(1, -1)
        area = np.sum(maskImg) // 255

        spectralData_A = spectralData_T / area  # 平均反射率
        spectralData_lgA = np.log10(spectralData_A)  # 平均反射率取对数
        spectralData_dA = HSI._dx_2nd_Order_Central(spectralData_A)  # 平均反射率一阶导
        spectralData_ddA = HSI._dx_2nd_Order_Central(spectralData_dA)  # 平均反射率二阶导
        spectralData_CommonSpectralIndex = HSI.CommonSpectralIndex(spectralData_A)  # 常见光谱指数

        traits = np.concatenate((spectralData_A, spectralData_dA, spectralData_ddA, spectralData_lgA,
                               spectralData_CommonSpectralIndex), axis=1).reshape(-1)
        return traits
