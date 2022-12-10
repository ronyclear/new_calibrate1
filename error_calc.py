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


f = open('./310114000001000001000000MEC000001CLO000001_cfg.json')
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

def calc_error(px_list, true_gps_list, cam_id):
    '''
    计算误差
    :param px_list: 测试像素点列表
    :param true_gps_list: 真实经纬度列表
    :return:
    '''
    gps_list = []
    for px in px_list:
        res = run(px[0], px[1], cam_id)
        gps_list.append(res)

    dst_list = []
    for real_pt, calc_pt in zip(true_gps_list, gps_list):
        dst = haversine([real_pt[1], real_pt[0]], [calc_pt[1], calc_pt[0]]) * 1000
        dst_list.append(dst)

    print('Error:', cam_id, np.average(dst_list))
    print(dst_list)


# camera_27
px_list_ = [[1709.3064516129027, 893.2077419354839], [685.0483870967739, 898.6270967741937], [1016.4998439125907, 269.00035757023943], [1421.675286160249, 249.4322254162331]]
px_list_arr = np.array(px_list_)
px_list = px_list_arr.tolist()
gps_list = [[121.22564636, 31.29345116], [121.22563563, 31.29351763], [121.22619018, 31.29354685], [121.22619487, 31.29348210]]
# camera_71
gps_list71 = [[121.22625321, 31.29357550], [121.22625455, 31.29351018], [121.22570269, 31.29346319], [121.22569531, 31.29355659]]
px_list_71_ =  [[1469.693548387097, 703.5303225806454], [648.661290322581, 668.3045161290324], [954.2386056191469, 226.0768383194591], [1184.7655046826226, 221.55670304370472]]
px_chg_71 = np.array(px_list_71_)
px_list_71 = px_chg_71.tolist()

px_31_list = [[842.2096774193546, 321.46580645161316], [69.95161290322574, 638.4980645161293], [460.14516129032245, 294.36903225806464], [1256.7903225806447, 302.49806451612926]]
gps_31_list = [[121.22590519, 31.29331364], [121.22584820, 31.29324373], [121.22584686, 31.29332911], [121.22596957, 31.29333198]]


for px_list, true_gps_list, car_id in zip([px_list_, px_list_71_, px_31_list], [gps_list, gps_list71, gps_31_list], ['dev11', 'dev21', 'dev31']):
    calc_error(px_list, true_gps_list, car_id)


