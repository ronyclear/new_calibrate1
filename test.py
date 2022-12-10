#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/10/14 15:14
# @Author  : xinguoron
# @Site    : 
# @File    : test.py
# @Software: PyCharm
# @email   : 1401255365@qq.com
from sympy.solvers import solve
from sympy import Symbol
from gaussReprojection import LatLon2XY, XY2LatLon
from calcu_params import get_params, get_expression
from haversine import haversine
import numpy as np



px_list_ = [[2912.290322580644, 1900.492903225806], [674.0967741935474, 1781.267096774193], [1499.5519250780433, 769.3265593132152], [2263.2788761706543, 763.3739224765866]]
px_list_arr = np.array(px_list_) / 2
px_list = px_list_arr.tolist()

gps_list = [[121.40716774935402, 31.243501817722173], [121.40709446724117, 31.243437355976546], [121.40660928911471, 31.243710721527442], [121.40665982850288, 31.243822932714274]]
xy_list_ = []
for gps_pt in gps_list:
    x,y = LatLon2XY(gps_pt[1], gps_pt[0])
    xy_list_.append([x,y])

xy_arr_ = np.array(xy_list_)
minxy = xy_arr_.min(axis=0)
res_arr = xy_arr_ - xy_arr_.min(axis=0) + 20
xy_list = res_arr.tolist()


params = get_params(xy_list, px_list)



# a = res.get('a')
# b = res.get('b')
# c = res.get('c')
# d = res.get('d')
# e = res.get('e')
# f = res.get('f')
# u = res.get('u')
# v = res.get('v')
# params =  [-0.0268555368865165, -0.0717246869639524, -0.0133404430303475, -0.480370125378873, -4.72596872901759, 173.686250390814, 8.94977047736478e-5, -0.00551637078446565]

# a,b,c,d,e,f,u,v = res

# params = list(res.values())
# print(params)
# print(res.values())
# print(a,b,c,d,e,f,u,v)

# print(lon,lat)
test_pt = [[691, 899], [672, 387],[1130,380]]
real_pt = [[121.40711188, 31.24345749],[121.40659221, 31.24368624], [121.40666127, 31.24382154]]

res_list = []
for px in test_pt:
    x, y = get_expression(params, px[0], px[1])

    x_t, y_t = x + minxy[0] - 20, y + minxy[1] - 20
    lat, lon = XY2LatLon(y_t, x_t, 120)
    res_list.append([lon, lat])

print(res_arr)
print(xy_list, px_list)
dst_list = []
for pt1, pt2 in zip(res_list, real_pt):
    dist = haversine([pt1[1],pt1[0]], [pt2[1], pt2[0]])
    dst_list.append(dist*1000)
print(dst_list)
print(np.average(dst_list))
print(res_list)