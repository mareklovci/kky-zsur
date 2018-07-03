#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Klasifikator s linearnimi diskriminacnimi funkcemi

* Rossenblattuv algoritmus
* metoda konstantnich prirustku
* upravena metoda konstantnich prirustku
"""

import logging
from zsur.genpoints import generate_points
from zsur.readfile import readfile
from zsur.kmeans import kmeans, plot_kmeans, update_list_dict
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_lines_constant_increment(data: dict, beta):
    logging.info('Generating lines coeficients')
    lines = dict.fromkeys(data, [1, 1, 1])  # vyhrazeni prostoru pro koeficienty primek
    for key, val in data.items():
        cont = True
        while cont:
            cont = False
            for k, v in data.items():
                q = 1 if key == k else -1
                for item in v:
                    x = np.array((1, item[0], item[1]))
                    if x.dot(lines[key]) * q < 0:
                        a = item[0]
                        b = item[1]
                        ck = beta / sqrt(a ^ 2 + b ^ 2)
                        lines[key] = np.transpose(lines[key]) + (ck * x * q)
                        cont = True
    lines = {k: tuple(v) for k, v in lines.items()}
    logging.info('Lines coeficients generated. {}'.format(lines))
    return lines


def merge_dicts(dict1: dict, dict2: dict):
    for k, v in dict2.items():
        if not v:
            continue
        else:
            dict1[k] = dict1[k] + v
    return dict1


def get_lines_ross(data: dict):
    logging.info('Generating lines coeficients')
    lines = dict.fromkeys(data)  # vyhrazeni prostoru pro koeficienty primek
    for key in lines:
        lines[key] = list((1, 1, 1))
    for key, val in data.items():
        for k, v in data.items():
            if key == k:
                q = 1
            else:
                q = -1
            for item in v:
                x = np.array((1, item[0], item[1]))
                li = lines[key]
                wec = x.dot(li)
                if wec * q < 0:
                    lines[key] = np.transpose(lines[key]) + (x * q)
    lines = {k: tuple(v) for k, v in lines.items()}
    logging.info('Lines coeficients generated - dict(point: coeficients). {}'.format(lines))
    return lines


def classify_ross(lines, trypoints):
    classified = dict.fromkeys(lines)
    for point in trypoints:
        sides = dict.fromkeys(lines)
        for key, val in lines.items():
            sides[key] = val[0] * point[0] + val[1] * point[1] + val[2]
        keys = [k for k, v in sides.items() if v < 0]
        if len(keys) > 1:
            continue
        elif len(keys) < 1:
            continue
        elif len(keys) == 1:
            update_list_dict(classified, keys[0], point)
    return classified


def rossenblatt(data, space_size=(-20, 20), step=1):
    lines = get_lines_ross(data)
    plot_lines(lines)
    trypoints = generate_points(space_size[0], space_size[1], step)
    classified = classify_ross(lines, trypoints)
    data = merge_dicts(data, classified)
    return data


def constant_increment(data, beta, space_size=(-20, 20), step=1):
    lines = get_lines_constant_increment(data, beta)
    plot_lines(lines)
    trypoints = generate_points(space_size[0], space_size[1], step)
    classified = classify_ross(lines, trypoints)
    data = merge_dicts(data, classified)
    return data


def plot_lines(lines: dict):
    t1 = np.arange(-20, 20, 1)
    for v in lines.values():
        plt.plot(t1, v[0]*t1 + v[1]*t1 + v[2])
    plt.ylim(-20, 20)
    plt.xlim(-20, 20)


def main():
    data = readfile('../data.txt')
    data = kmeans(data, 3)
    ross = rossenblatt(data)
    plot_kmeans(ross)
    # const_incr = constant_increment(data, 0.5)
    # plot_kmeans(const_incr)


if __name__ == '__main__':
    main()
