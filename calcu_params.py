#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 10:09
# @Author  : xinguoron
# @Site    : 
# @File    : calcu_params.py
# @Software: PyCharm
# @email   : 1401255365@qq.com

from sympy.solvers import solve
from sympy import Symbol
import numpy as np
import json
from gaussReprojection import LatLon2XY, XY2LatLon


def get_expression(params,x,y):
    '''获取表达式'''
    a,b,c,d,e,f,u,v = params
    ex_x = (a * x + b * y + e) / (1 + u * x + v * y)
    ex_y = (c * x + d * y + f) / (1 + u * x + v * y)
    return ex_x, ex_y


def get_params(xy_list, uv_list):
    a = Symbol("a")
    b = Symbol("b")
    c = Symbol("c")
    d = Symbol("d")
    e = Symbol("e")
    f = Symbol("f")
    u = Symbol("u")
    v = Symbol("v")


    # xy_list = [[12,12], [13,14],[19,24],[22,19]]
    # uv_list = [[23,23], [45,45], [43,5], [4,5]]
    expression = []
    for xy_pt, uv_pt in zip(xy_list, uv_list):
        x = uv_pt[0]  # 图像坐标
        y = uv_pt[1]

        x_ = xy_pt[0]  # 地面坐标
        y_ = xy_pt[1]

        ex_x = (a* x + b*y + e)/(1+u*x + v*y) - x_
        ex_y = (c*x + d*y + f) / (1+u*x + v*y) - y_

        expression.append(ex_x)
        expression.append(ex_y)
    args = [a, b, c, d, e, f, u, v]
    res = solve(expression, args)

    return list(res.values())


def run(gps_list, px_list):
    xy_list_ = []
    for gps_pt in gps_list:
        x, y = LatLon2XY(gps_pt[1], gps_pt[0])
        xy_list_.append([x, y])

    xy_arr_ = np.array(xy_list_)
    minxy = xy_arr_.min(axis=0)
    res_arr = xy_arr_ - xy_arr_.min(axis=0) + 20
    xy_list = res_arr.tolist()
    params = get_params(xy_list, px_list)

    return params, minxy


def calibrate_multi_cameras(camera_id_list, cali_data_list, crossId):
    '''
    :param camera_id_list: 相机的设备代码      cam1                cam2         ...
    :param cali_data_list: 标定的数据，[[gps_list, px_list],[gps_list, px_list]]
    :return: 将参数存为json文件
    '''
    total_cfg_list = {}
    for cam_name, cali_data in zip(camera_id_list, cali_data_list):
        params, minxy = run(cali_data[0], cali_data[1])
        this_cam_param = {'a': params[0], 'b':params[1], 'c':params[2],
                          'd':params[3], 'e':params[4], 'f':params[5],
                          'u':params[6], 'v':params[7], 'minx': minxy[0], 'miny': minxy[1]}
        total_cfg_list[cam_name] = this_cam_param
    print(total_cfg_list)
    with open(f'{crossId}_cfg.json', 'w') as f:
        # total_cfg_list = json.dumps(total_cfg_list)
        f.write(json.dumps(str(total_cfg_list)))



# 东：dev11
# 西：dev21
# 北：dev41
# 南：dev31

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

px_31_list = [[1506.08064516129, 652.0464516129034], [69.95161290322574, 638.4980645161293], [460.14516129032245, 294.36903225806464], [1256.7903225806447, 302.49806451612926]]
gps_31_list = [[121.22597158, 31.29324603], [121.22584820, 31.29324373], [121.22584686, 31.29332911], [121.22596957, 31.29333198]]

camera_id_list = ['dev11', 'dev21', 'dev31']
cali_data_list = [[gps_list, px_list], [gps_list71,px_list_71], [gps_31_list, px_31_list]]
calibrate_multi_cameras(camera_id_list, cali_data_list, '310114000001000001000000MEC000001CLO000001')

# calibrate_multi_cameras
# params,minxy = run(gps_list, px_list)
# print(params,minxy)

#
# #求出的结果
# print(res)
# print(expression)
# # 测试结果是否正确
#
# a = res.get(a)
# b = res.get(b)
# c = res.get(c)
# d = res.get(d)
# e = res.get(e)
# f = res.get(f)
# u = res.get(u)
# v = res.get(v)
#
# print(a,b,c,d,e,f,u,v)
# print((23*a + 23*b + e)/(23*u + 23*v + 1) - 12)
# print((23*c + 23*d + f)/(23*u + 23*v + 1) - 12)
# print(10 * a + 6 * b + 5 * c + 2 * e)
# print(6 * a + 2 * b + 6 * c + 6 * e)
# print(13 * a + 11 * b + 9 * c + 2 * e)
# print(11*a+9*b+7*c+4*d+2*e)
# print(8 * a + 8 * b + 5 * c + 2 * d + e)

