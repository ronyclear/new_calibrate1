# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 10:29
# @Author  : xinguoron
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @email   : 1401255365@qq.com
import numpy as np
import json
import math
from haversine import haversine


def get_expression(params, x, y):
    '''获取表达式'''
    a, b, c, d, e, f, u, v = params['a'], params['b'], params['c'], params['d'], params['e'], params['f'], params['u'], \
                             params['v']
    ex_x = (a * x + b * y + e) / (1 + u * x + v * y)
    ex_y = (c * x + d * y + f) / (1 + u * x + v * y)
    return ex_x, ex_y


def XY2LatLon(X, Y, L0):
    iPI = 0.0174532925199433
    a = 6378137.0
    f = 0.00335281006247
    ZoneWide = 3  # 按3度带进行投影

    ProjNo = int(X / 1000000)
    L0 = L0 * iPI
    X0 = ProjNo * 1000000 + 500000
    Y0 = 0
    xval = X - X0
    yval = Y - Y0

    e2 = 2 * f - f * f  # 第一偏心率平方
    e1 = (1.0 - math.sqrt(1 - e2)) / (1.0 + math.sqrt(1 - e2))
    ee = e2 / (1 - e2)  # 第二偏心率平方

    M = yval
    u = M / (a * (1 - e2 / 4 - 3 * e2 * e2 / 64 - 5 * e2 * e2 * e2 / 256))

    fai = u \
          + (3 * e1 / 2 - 27 * e1 * e1 * e1 / 32) * math.sin(2 * u) \
          + (21 * e1 * e1 / 16 - 55 * e1 * e1 * e1 * e1 / 32) * math.sin(4 * u) \
          + (151 * e1 * e1 * e1 / 96) * math.sin(6 * u) \
          + (1097 * e1 * e1 * e1 * e1 / 512) * math.sin(8 * u)
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

    # 换换为deg
    longitude = longitude1 / iPI
    latitude = latitude1 / iPI

    return latitude, longitude


f = open('./31011600088_cfg.json')
params = json.load(f)
f.close()


def run(x, y, cam_id):
    # 若当前相机已经标定好
    if cam_id in params:
        this_cam_param = eval(params)[cam_id]  #
        ground_x, ground_y = get_expression(this_cam_param, x, y)
        minx = this_cam_param['minx']
        miny = this_cam_param['miny']

        x_t, y_t = ground_x + minx - 20, ground_y + miny - 20
        lat, lon = XY2LatLon(y_t, x_t, 120)
        return lon, lat
    else:  # 若未标定好，则返回0,0
        return 0, 0



test_pt1 = [321, 381]
real_pt1 = [121.40716888, 31.24349992]

test_pt2 = [1004, 399]
real_pt2 = [121.40707165, 31.24341163]

res1 = run(test_pt1[0], test_pt1[1], 'dev71')
res2 = run(test_pt2[0], test_pt2[1], 'dev71')
print(f'{test_pt1}转换后的经纬度：{res1}')
print(f'{test_pt2}转换后的经纬度：{res2}')
dst_list = []
for real_pt, calc_pt in zip([real_pt1, real_pt2], [res1, res2]):
    dst = haversine([real_pt[1], real_pt[0]], [calc_pt[1], calc_pt[0]]) * 1000
    dst_list.append(dst)

print(np.average(dst_list))
print(dst_list)
