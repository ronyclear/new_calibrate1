#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 16:50
# @Author  : xinguoron
# @Site    : 
# @File    :
# @Software: PyCharm
# @email   : 1401255365@qq.com

import matplotlib.pyplot as plt
from osgeo import ogr
from matplotlib.image import imread
from gaussReprojection import LatLon2XY
# from tsai import TsaiCameraCalibrate as tsaiCali
import numpy as np
import json
import os
# from uiTool import getParams
import random
# from getOutPixel import getCameraResolution
# from pxToGpsCali import transformGO
from math import radians, cos,asin,sqrt,sin

# 获取UI得到的参数
# params = getParams()
# # print('params:', params)
# cmos_size = params['cmos_size']
# image_width = params['image_width'] # 原始图片尺寸
# image_height = params['image_height']
# ip = params['ip']
# # print(1, ip)
# TrafficMarkings = params['TrafficMarkings'] # 高精度地图文件夹
# DirectionArrow = params['DirectionArrow']
# PavementSymbolMarkings = params['PavementSymbolMarkings']
# TrafficMarkings_CrossWalk = params['TrafficMarkings_CrossWalk']
# image_path = params['image_path'] # 图片路径


ax1_click_no = 1
ax2_click_no = 1


def calibrateTool(image1_path, image2_path):
    # 分辨率及cmos尺寸
    # reso, cmosSize = getCameraResolution(projectName, ip)
    #
    # # global ax1_click_no, ax2_click_no
    # def plot_point(point, symbol='ko', **kwargs):
    #     x, y = point.GetX(), point.GetY()
    #     ax1.plot(x, y, symbol, **kwargs)
    #
    # def plot_line(line, symbol='g-', **kwargs):
    #     x, y = zip(*line.GetPoints())
    #     ax1.plot(x, y, symbol, **kwargs)
    #
    # def plot_polygon(poly, symbol='r-', **kwargs):
    #     for i in range(poly.GetGeometryCount()):
    #         subgeom = poly.GetGeometryRef(i)
    #         x, y = zip(*subgeom.GetPoints())
    #         ax1.plot(x, y, symbol, **kwargs)
    #
    # def plot_layer(filename, symbol, layer_index=0, **kwargs):
    #     ds = ogr.Open(filename)
    #     for row in ds.GetLayer(layer_index):
    #         geom = row.geometry()
    #         geom_type = geom.GetGeometryType()
    #
    #         if geom_type == ogr.wkbPoint:
    #             plot_point(geom, symbol, **kwargs)
    #         elif geom_type == ogr.wkbMultiPoint:
    #             for i in range(geom.GetGeometryCount()):
    #                 subgeom = geom.GetGeometryRef(i)
    #                 plot_point(subgeom, symbol, **kwargs)
    #
    #         elif geom_type == ogr.wkbLineString:
    #             plot_line(geom, symbol, **kwargs)
    #         elif geom_type == ogr.wkbMultiLineString:
    #             for i in range(geom.GetGeometryCount()):
    #                 subgeom = geom.GetGeometryRef(i)
    #                 plot_line(subgeom, symbol, **kwargs)
    #
    #         elif geom_type == ogr.wkbPolygon:
    #             plot_polygon(geom, symbol, **kwargs)
    #         elif geom_type == ogr.wkbMultiPolygon:
    #             for i in range(geom.GetGeometryCount()):
    #                 subgeom = geom.GetGeometryRef(i)
    #                 plot_polygon(subgeom, symbol, **kwargs)

    gpsPtList = []
    pixPtList = []

    fig = plt.figure()

    fig.canvas.set_window_title('res')
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=None)

    ax1 = fig.add_subplot(1, 2, 1)
    ax2 = fig.add_subplot(1, 2, 2)

    # ax1.set_title('SELECT GPS POINTS')

    ax1.set_title('select_key_point')
    img1 = imread(image1_path)
    # img1_size = img1.shape()
    ax1.imshow(img1)

    ax2.set_title('res')
    img2 = imread(image2_path)
    # imgSize = img2.shape
    # print('图片的大小为：', img.shape)
    ax2.imshow(img2)

    # def plotShapefile():
    #     # basedir = './SHP'
    #     # 下面三个谁在上边就先显示谁
    #     colorList = ['k-', 'r-', 'g-', 'b-']
    #     for obj in shpPathList:
    #         plot_layer(obj, random.choice(colorList), markersize=0.5)
    #         # plot_layer(DirectionArrow,'r-')
    #         # plot_layer(PavementSymbolMarkings,'g-',markersize=0.05)
    #         # plot_layer(TrafficMarkings_CrossWalk, 'b-')
    #     # plt.axis('equal')
    #     plt.gca().get_xaxis().set_ticks([])
    #     plt.gca().get_yaxis().set_ticks([])

    def onclick(event):
        global ax1_click_no, ax2_click_no
        if event.inaxes == ax1:
            gpsPtList.append([event.xdata, event.ydata])
            ax1.plot(event.xdata, event.ydata, 'o', markersize=8)
            ax1.annotate(str(ax1_click_no), (event.xdata, event.ydata))
            ax1_click_no += 1
        else:
            # print('processing on draw pts')
            pixPtList.append([event.xdata, event.ydata])
            ax2.plot(event.xdata, event.ydata, 'o', markersize=8)
            ax2.annotate(str(ax2_click_no), (event.xdata, event.ydata))
            ax2_click_no += 1
        fig.canvas.draw()

    # plotShapefile()
    cid = fig.canvas.mpl_connect('key_press_event', onclick)
    plt.show()
    return gpsPtList, pixPtList

# image1_path = './1.jpg'  # 曹杨路标定
# image2_path = './2.jpg'

image1_path = './YANGLINLU/3100.png'  # 杨林路标定
image2_path = './YANGLINLU/2100.png'
img1PtList, img2PtList = calibrateTool(image1_path, image2_path)

print('img1:, \n\n')
print(img1PtList)

print('img2:, \n\n')
print(img2PtList)

    # def pxPtsTransform(rawImg):
    #     '''
    #     rawImg为传感器采集到的原始的图片尺寸，dtype为行、列排序，e.g.(4096,2160)
    #     :param rawImg:
    #     :return:
    #     '''
    #     rawImgWidth = rawImg[0]
    #     rawImgLength = rawImg[1]
    #     showImgWidth = imgSize[1]
    #     showImgLength = imgSize[0]
    #     if showImgWidth == rawImgWidth:
    #         return pixPtList
    #     else:
    #         return [[obj[0] * rawImgWidth / showImgWidth, obj[1] * rawImgLength / showImgLength] for obj in pixPtList]
    #
    # def geodistance(pt1, pt2):
    #     lng1, lat1 = pt1
    #     lng2, lat2 = pt2
    #     lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)])  # 经纬度转换成弧度
    #     dlon = lng2 - lng1
    #     dlat = lat2 - lat1
    #     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    #     distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    #     # distance=round(distance/1000,3)
    #     return distance
    #
    #
    # def lnglat2xy():
    #     if len(gpsPtList) > 0:
    #         xyList = []
    #         for pt in gpsPtList:
    #             x, y = LatLon2XY(pt[1], pt[0])
    #             xyList.append([x, y])
    #         xyArr = np.array(xyList)
    #         minx, miny = xyArr.min(axis=0)
    #         operatedXY = xyArr - xyArr.min(axis=0) + 50
    #         return operatedXY.tolist(), [minx, miny]
    #     else:
    #         return [], []
    #
    #
    # def createPixFilterPackage(projName, roadNo, filePackageName):
    #     '''根据项目名称、路口号新建存单个相机的过滤json文件'''
    #     targetDir = os.path.join('./data', projName, filePackageName, str(roadNo))
    #     if not os.path.exists(targetDir):
    #         os.mkdir(targetDir)
    #
    # def getCameraParams(rawImgSize, sensorSize):
    #     createPixFilterPackage(projectName, roadNo, 'camera_calibrate_result')
    #     savePath = os.path.join('./data/', projectName, 'camera_calibrate_result', str(roadNo), ip + '.json')
    #     thisRoadLogDir = os.path.join('./data/', projectName, 'logs', str(roadNo))
    #     if not os.path.exists(thisRoadLogDir):
    #         os.mkdir(thisRoadLogDir)
    #     logSavePath = os.path.join('./data/', projectName, 'logs', str(roadNo), ip + '.txt')
    #     fwLog = open(logSavePath, 'w')
    #     getPXData = pxPtsTransform(rawImgSize)
    #     getXYData, minxy = lnglat2xy()
    #     if len(getPXData) == len(getXYData) and len(getPXData) >= 6:
    #         calibrateRes = tsaiCali(rawImgSize, np.array(getPXData), np.array(getXYData), sensorSize).getExactfTzK1()
    #         calibrateRes['minX'] = minxy[0]
    #         calibrateRes['minY'] = minxy[1]
    #         caliCheckLngLat = [transformGO(calibrateRes, obj[0], obj[1]) for obj in getPXData]
    #         # 计算算出的经纬度和实际的经纬度的距离
    #         err = np.mean([geodistance(gpsPtList[ind], caliCheckLngLat[ind]) for ind in range(len(caliCheckLngLat))])
    #         writeMsg = '拾取的像素坐标：' + '\n' + str(getPXData) + '\n\n' + '拾取的路面坐标：' + '\n' + str(getXYData) + \
    #                    '\n' + '原点：\n' + str(minxy) + '\n\n' + 'error:' + str(err) + '\n\noutGPS：' + '\n' + str(caliCheckLngLat)
    #         fwLog.write(writeMsg)
    #         fwLog.close()
    #         if calibrateRes != 'failed':
    #             calibrateRes['ip'] = ip
    #             fw = open(savePath, 'w', encoding='utf-8')
    #             json.dump(calibrateRes, fw)
    #             fw.close()
    #         return calibrateRes
    #     else:
    #         return 'failed'

    # return getCameraParams(rowImgSize, cmosSize)

