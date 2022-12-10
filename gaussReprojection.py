#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 17:17
# @Author  : xinguoron
# @Site    : 
# @File    : gaussianReprojection.py
# @Software: PyCharm
# @email   : 1401255365@qq.com

import math


def LatLon2XY(latitude, longitude):
  a = 6378137.0
  # b = 6356752.3142
  # c = 6399593.6258
  # alpha = 1 / 298.257223563
  e2 = 0.0066943799013
  # epep = 0.00673949674227

  #将经纬度转换为弧度
  latitude2Rad = (math.pi / 180.0) * latitude

  beltNo = int((longitude + 1.5) / 3.0) #计算3度带投影度带号
  L = beltNo * 3 #计算中央经线
  l0 = longitude - L #经差
  tsin = math.sin(latitude2Rad)
  tcos = math.cos(latitude2Rad)
  t = math.tan(latitude2Rad)
  m = (math.pi / 180.0) * l0 * tcos
  et2 = e2 * pow(tcos, 2)
  et3 = e2 * pow(tsin, 2)
  X = 111132.9558 * latitude - 16038.6496 * math.sin(2 * latitude2Rad) + 16.8607 * math.sin(
    4 * latitude2Rad) - 0.0220 * math.sin(6 * latitude2Rad)
  N = a / math.sqrt(1 - et3)

  x = X + N * t * (0.5 * pow(m, 2) + (5.0 - pow(t, 2) + 9.0 * et2 + 4 * pow(et2, 2)) * pow(m, 4) / 24.0 + (
  61.0 - 58.0 * pow(t, 2) + pow(t, 4)) * pow(m, 6) / 720.0)
  y = 500000 + N * (m + (1.0 - pow(t, 2) + et2) * pow(m, 3) / 6.0 + (
  5.0 - 18.0 * pow(t, 2) + pow(t, 4) + 14.0 * et2 - 58.0 * et2 * pow(t, 2)) * pow(m, 5) / 120.0)
  return x, y


def XY2LatLon(X, Y, L0):

  iPI = 0.0174532925199433
  a = 6378137.0
  f= 0.00335281006247
  ZoneWide = 3 #按3度带进行投影

  ProjNo = int(X / 1000000)
  L0 = L0 * iPI
  X0 = ProjNo * 1000000 + 500000
  Y0 = 0
  xval = X - X0
  yval = Y - Y0

  e2 = 2 * f - f * f #第一偏心率平方
  e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
  ee = e2 / (1 - e2) #第二偏心率平方

  M = yval
  u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))

  fai = u \
     + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) \
     + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) \
     + (151 * e1 * e1 * e1 / 96) * math.sin(6 * u)\
     + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(8 * u)
  C = ee * math.cos(fai) * math.cos(fai)
  T = math.tan(fai) * math.tan(fai)
  NN = a / math.sqrt(1.0 - e2 * math.sin(fai) * math.sin(fai))
  R = a * (1 - e2) / math.sqrt(
    (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)))
  D = xval / NN

  #计算经纬度（弧度单位的经纬度）
  longitude1 = L0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (
  5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / math.cos(fai)
  latitude1 = fai - (NN * math.tan(fai) / R) * (
  D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (
  61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)

  #换换为deg
  longitude = longitude1 / iPI
  latitude = latitude1 / iPI

  return latitude, longitude


class XYexchangeBL:
    def get_WGS84_af(self):
        a = 6378137.0
        f = 1 / 298.257223563
        return a, f

    def XY2LatLon(self, ellipsoid, X, Y, L0):
        # 椭圆参数控制
        if (ellipsoid == 84):
            a, f = self.get_WGS84_af()

        iPI = 0.0174532925199433333333  # 圆周率/180
        ProjNo = int(X / 1000000)
        L0 = L0 * iPI

        X0 = ProjNo * 1000000 + 500000  # 东偏500000为后续步骤减去做铺垫
        Y0 = 0
        xval = X - X0
        yval = Y - Y0

        e2 = 0.00669437999013
        e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
        ee = 0.00673949674223
        M = yval
        u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))
        # "\"表示转公式下一行结合在一起
        fai = u + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) + (
                21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) + (
                      151 * e1 * e1 * e1 / 96) * math.sin(6 * u) + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(
            8 * u)
        C = ee * math.cos(fai) * math.cos(fai)
        T = math.tan(fai) * math.tan(fai)
        NN = a / math.sqrt(1.0 - e2 * math.sin(fai) * math.sin(fai))
        R = a * (1 - e2) / math.sqrt(
            (1 - e2 * math.sin(fai) * math.sin(fai)) * (1 - e2 * math.sin(fai) * math.sin(fai)) * (
                    1 - e2 * math.sin(fai) * math.sin(fai)))
        D = xval / NN
        # 计算经纬度（弧度单位的经纬度）
        longitude1 = L0 + (D - (1 + 2 * T + C) * D * D * D / 6 + (
                5 - 2 * C + 28 * T - 3 * C * C + 8 * ee + 24 * T * T) * D * D * D * D * D / 120) / math.cos(fai)
        latitude1 = fai - (NN * math.tan(fai) / R) * (
                D * D / 2 - (5 + 3 * T + 10 * C - 4 * C * C - 9 * ee) * D * D * D * D / 24 + (
                61 + 90 * T + 298 * C + 45 * T * T - 256 * ee - 3 * C * C) * D * D * D * D * D * D / 720)
        longitude = longitude1 / iPI
        latitude = latitude1 / iPI
        return longitude, latitude


from math import radians, cos, sin, asin, sqrt

#公式计算两点间距离（m）

def geodistance(pt1, pt2):
    lng1, lat1 = pt1
    lng2, lat2 = pt2
    lng1, lat1, lng2, lat2 = map(radians, [float(lng1), float(lat1), float(lng2), float(lat2)]) # 经纬度转换成弧度
    dlon=lng2-lng1
    dlat=lat2-lat1
    a=sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    distance=2*asin(sqrt(a))*6371*1000 # 地球平均半径，6371km
    # distance=round(distance/1000,3)
    return distance



#
# testPt = [120.15071556, 30.86119707]
# x,y = LatLon2XY(testPt[1], testPt[0])
#
# xRaw, yRaw = XY2LatLon(y, x, 120)
#
# xy22BL= XYexchangeBL()
# xNew, yNew = xy22BL.XY2LatLon(84, y, x, 120)
#
# print(x,y)
# print(yRaw, xRaw)
# print(xNew, yNew)
#
# dst = geodistance([yRaw, xRaw], [xNew, yNew])
# print(dst)