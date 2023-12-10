# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import math
from skimage import morphology

import paddle
import pickle
import cv2
import sys
import os
import numpy as np

from paddleseg.cvlibs import Config
from paddleseg.utils import get_sys_env, logger, utils
from paddleseg.core import infer

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

transformsPth = os.path.join(base_path, 'myconfig', 'transforms.pkl')
modelPth = os.path.join(base_path, 'myconfig', 'segformer_cotton_root_1024x1024_150k.yml') 
modelParams = os.path.join(base_path, 'myconfig', 'model.pdparams')


def myPredict(image):
    env_info = get_sys_env()
    place = 'gpu' if env_info['Paddle compiled with cuda'] and env_info[
        'GPUs used'] else 'cpu'

    paddle.set_device(place)
    with open(transformsPth, 'rb') as f:
        transforms = pickle.load(f)

    model = Config(modelPth).model
    utils.load_entire_model(model, modelParams)
    model.eval()

    logger.info("Start to predict...")
    with paddle.no_grad():
        im = image
        ori_shape = im.shape[:2]
        im, _ = transforms(im)
        im = im[np.newaxis, ...]
        im = paddle.to_tensor(im)
        pred = infer.inference(
            model,
            im,
            ori_shape=ori_shape,
            transforms=transforms.transforms,
            is_slide=True,
            stride=[400, 400],
            crop_size=[512, 512])
        pred = paddle.squeeze(pred)
        pred = pred.numpy().astype('uint8')
        pred[pred != 0] = 255
        return pred


def getSegImg(img):

    def _dilate(img, kernelsize=3, iterations=10):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernelsize, kernelsize))
        dilated = cv2.dilate(img, kernel, iterations=iterations)
        return dilated

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

    segImg = myPredict(img)
    _, bwImg = cv2.threshold(segImg, 1, 255, cv2.THRESH_BINARY)
    # bwImg = _dilate(bwImg, 3, 10)
    bwImg = _removesmall(bwImg, 700)
    return bwImg


def getHeader():
    head = ['area', 'convex_area', 'length', 'depth', 'width', 'wdRatio', 'centroid_x', 'centroid_y', 'sturdiness',
            'mass_2_L1', 'mass_2_L2', 'mass_2_L_Ratio', 'mass_3_L1', 'mass_3_L2', 'mass_3_L_Ratio',
            'density_1_1', 'density_1_2', 'density_2_1', 'density_2_2', 'density_3_1', 'density_3_2',
            'angle_top_left', 'angle_top_right', 'angle_top_all', 'shape_1', 'angle_entire_left', 'angle_entire_right', 'angle_entire_all', 'shape_2'
            ]
    return head

def calcTraits(bwImg):
    def _calcalate_angle2(point1, point2, point3):
        if point2[0] - point1[0]:
            tanup = (point2[1] - point1[1]) / (point2[0] - point1[0])
            angleup = math.atan(tanup)
            angleup = angleup / math.pi * 180
        else:
            angleup = 90
        if point3[0] - point1[0]:
            tandown = (point3[1] - point1[1]) / (point3[0] - point1[0])
            angledown = math.atan(tandown)
            angledown = angledown / math.pi * 180
        else:
            angledown = -90

        if angleup == 'nan':
            angleup = 0

        if angledown == 'nan':
            angledown = 0

        return angleup, angledown

    def _get_angles(bw):
        contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        contours_all = []
        for contour in contours:
            for contour_index in contour:
                contours_all.append(contour_index)
        points = np.array(contours_all)
        hull = cv2.convexHull(points)
        point1 = []
        for point in hull:
            point1.append((point[0][0], point[0][1]))
        point1.sort(key=lambda x: x[0], reverse=True)
        # point1 = point_mining(point1)
        contours_all2 = point1.copy()
        contours_all2.pop(0)
        contours_all2.sort(key=lambda x: (x[1], x[0]), reverse=True)
        max_down_point = contours_all2[0]
        contours_all2.sort(key=lambda x: (x[1], 1 / x[0]))
        max_top_point = contours_all2[0]

        black_img = np.zeros(bw.shape)
        cv2.polylines(black_img, [hull], True, 255, 1)
        hull_all_arr = np.argwhere(black_img == 255)
        start = point1[0]
        up_points = []
        for i in range(10, 100, 20):
            po = [(y, x) for y, x in hull_all_arr if x == start[0] - i if y < start[1]]
            if po:
                up_points.append(np.mean(po, 0))
        down_points = []
        for i in range(10, 100, 20):
            po = [(y, x) for y, x in hull_all_arr if x == start[0] - i if y > start[1]]
            if po:
                down_points.append(np.mean(po, 0))
        if up_points and down_points:
            up_point = np.mean(up_points, 0, np.int32)
            up_point = up_point[::-1]
            down_point = np.mean(down_points, 0, np.int32)
            down_point = down_point[::-1]
            angle_up_top, angle_down_top = _calcalate_angle2(point1[0], list(up_point), list(down_point))
            angle_up_entire, angle_down_entire = _calcalate_angle2(point1[0], list(max_top_point), list(max_down_point))
        else:
            angle_up_top, angle_down_top, angle_up_entire, angle_down_entire = [0] * 4
        return start, angle_up_top, angle_down_top, angle_up_entire, angle_down_entire

    def _get_biomass(skeleton, start):
        info = []
        for line in [1800, 2700]:
            skeleton_20 = skeleton[:, start[0] - line:start[0]]
            skeleton20_ = skeleton[:, :start[0] - line]
            mass_L1 = len(np.argwhere(skeleton_20 == 255))
            mass_L2 = len(np.argwhere(skeleton20_ == 255))
            mass_L_Ratio = mass_L2 / mass_L1 if mass_L1 else 0
            info += [mass_L1, mass_L2, mass_L_Ratio]
        return info

    def _get_density(bwImg, img_convex, start):
        info = []
        for line in [900,  1800, 2700]:
            img_20 = bwImg[:, start[0] - line:start[0]]
            img20_ = bwImg[:, :start[0] - line]
            mass_A1 = len(np.argwhere(img_20 == 255))
            mass_A2 = len(np.argwhere(img20_ == 255))
            if mass_A1:
                density_1 = len(np.argwhere(img_convex[:, start[0] - line:start[0]])) / mass_A1
            else:
                density_1 = 0
            if mass_A2:
                density_2 = len(np.argwhere(img_convex[:, :start[0] - line])) / mass_A2
            else:
                density_2 = 0
            info += [density_1, density_2]
        return info

    traits = []
    start, angle_top_left, angle_top_right, angle_entire_left, angle_entire_right = _get_angles(bwImg)

    # area #
    arr = np.argwhere(bwImg == 255)
    area = arr.shape[0]
    traits.append(area)

    hull = np.squeeze(cv2.convexHull(arr[:, :2]), axis=1)

    # convex_area #
    hull_trs = np.asarray([[i[1], i[0]] for i in hull])
    img_convex = np.zeros(bwImg.shape, np.uint8)
    cv2.fillConvexPoly(img_convex, hull_trs, [255])
    arr_1 = np.argwhere(img_convex == 255)
    convex_area = arr_1.shape[0]
    traits.append(convex_area)

    # length #
    img_skeleton = bwImg.copy()
    img_skeleton[img_skeleton == 255] = 1
    skeleton0 = morphology.skeletonize(img_skeleton)
    skeleton = skeleton0.astype(np.uint8) * 255
    arr_skeleton = np.argwhere(skeleton == 255)
    length = arr_skeleton.shape[0]
    traits.append(length)

    # depth, width, wdRatio #
    w_min, d_min = np.min(arr, axis=0)
    w_max, d_max = np.max(arr, axis=0)
    width = w_max - w_min
    depth = d_max - d_min
    wdRatio = width / depth
    traits += [depth, width, wdRatio]

    # centroid_x, centroid_y #
    centroid_xy = np.sum(arr, axis=0) / area
    centroid_x = centroid_xy[0] - start[1]
    centroid_y = start[0] - centroid_xy[1]
    traits += [centroid_x, centroid_y]

    # sturdiness #
    sturdiness = length / convex_area
    traits.append(sturdiness)

    # mass_2_L1, mass_2_L2, mass_2_L_Ratio, mass_3_L1, mass_3_L2, mass_3_L_Ratio #
    biomass = _get_biomass(skeleton, start)
    traits += biomass

    # density_1_1, density_1_2, density_2_1, density_2_2, density_3_1, density_3_2 #
    density = _get_density(bwImg, img_convex, start)
    traits += density

    # angle_top_left, angle_top_right, angle_top_all, shape_1, angle_entire_left, angle_entire_right, angle_entire_all, shape_2 #
    angle_top_all = angle_top_left - angle_top_right
    angle_entire_all = angle_entire_left - angle_entire_right
    shape_1 = angle_top_all * 100 / depth
    shape_2 = angle_entire_all * 100 / depth
    traits += [angle_top_left, angle_top_right, angle_top_all, shape_1, angle_entire_left, angle_entire_right, angle_entire_all, shape_2]

    return traits


if __name__ == '__main__':
    imgPth = r"./D.png"
    image = cv2.imread(imgPth)
    pred = myPredict(image)
    cv2.imwrite("test.png", pred)
