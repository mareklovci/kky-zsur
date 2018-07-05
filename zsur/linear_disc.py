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
    lines = _get_default_lines(data)
    for key in data.keys():
        cont = True
        while cont:
            cont = False
            for k, v in data.items():
                q = 1 if key == k else -1
                for item in v:
                    x = np.array((1, item[0], item[1]))
                    if x.dot(lines[key]) * q < 0:
                        if (item[0] and item[1]) != 0:
                            ck = beta / sqrt(item[0]**2 + item[1]**2)
                        else:
                            continue
                        lines[key] = np.transpose(lines[key]) + (ck * x * q)
                        cont = True
    lines = {k: tuple(v) for k, v in lines.items()}
    logging.info('Lines coeficients generated. {}'.format(lines))
    return lines


def get_lines_modified_constant_increment(data: dict, beta):
    logging.info('Generating lines coeficients')
    lines = _get_default_lines(data)
    for key in data.keys():
        cont = True
        while cont:
            cont = False
            for k, v in data.items():
                q = 1 if key == k else -1
                for item in v:
                    x = np.array((1, item[0], item[1]))
                    if x.dot(lines[key])*q < 0:
                        ok = False
                        while not ok:
                            if (item[0] and item[1]) != 0:
                                ck = beta / sqrt(item[0] ** 2 + item[1] ** 2)
                            else:
                                continue
                            lines[key] = np.transpose(lines[key]) + (ck * x * q)
                            if x.dot(lines[key])*q >= 0:
                                ok = True
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
    lines = _get_default_lines(data)
    for key, val in data.items():
        itera = 0
        logging.info('get_lines - key: {}'.format(key))
        cont = True
        while cont:
            logging.info('get_lines - iter: {}'.format(itera))
            itera += 1
            cont = False
            for k, v in data.items():
                q = 1 if key == k else -1
                for item in v:
                    x = np.array((1, item[0], item[1]))
                    li = np.array(lines[key])
                    if li.dot(x) * q < 0:
                        lines[key] = np.transpose(lines[key]) + (x * q)
                        cont = True
    lines = {k: tuple(v) for k, v in lines.items()}  # from numpy to normal python
    logging.info('Lines coeficients generated - dict(point: coeficients). {}'.format(lines))
    return lines


def _get_default_lines(data: dict):
    lines = dict.fromkeys(data)  # vyhrazeni prostoru pro koeficienty primek
    for key in lines:
        lines[key] = list((1, 1, 1))
    return lines


def representatives(data: dict, lines: dict):
    vzory = dict.fromkeys(data)
    for key in data.keys():
        tmp = [1, 1, 1]
        x = data[key][0]
        no = 0
        for k in lines.keys():
            tmp[no] = 1 if x[1] > (lines[k][0] + x[0] * lines[k][1]) / -lines[k][2] else 0
            no += 1
        vzory[key] = tmp
    return vzory


def classify_ross(lines, trypoints, repre):
    classified = dict.fromkeys(lines)
    for k in trypoints:
        stavajici = dict.fromkeys(lines)
        for j in lines.keys():
            if k[1] > (lines[j][0] + k[0] * lines[j][1])/-lines[j][2]:
                stavajici[j] = 1
            else:
                stavajici[j] = 0
        for j in repre.keys():
            if repre[j] == list(stavajici.values()):
                update_list_dict(classified, j, k)
    return classified


def rossenblatt(data, space_size=(-20, 20), step=1):
    lines = get_lines_ross(data)
    # plot_lines(lines)  # needs some fixing, but algorithm is ok
    repre = representatives(data, lines)
    trypoints = generate_points(space_size[0], space_size[1], step)
    classified = classify_ross(lines, trypoints, repre)
    data = merge_dicts(data, classified)
    return data


def constant_increment(data, beta, space_size=(-20, 20), step=1):
    lines = get_lines_constant_increment(data, beta)
    repre = representatives(data, lines)
    trypoints = generate_points(space_size[0], space_size[1], step)
    classified = classify_ross(lines, trypoints, repre)
    data = merge_dicts(data, classified)
    return data


def modified_constant_increment(data, beta, space_size=(-20, 20), step=1):
    lines = get_lines_modified_constant_increment(data, beta)
    repre = representatives(data, lines)
    trypoints = generate_points(space_size[0], space_size[1], step)
    classified = classify_ross(lines, trypoints, repre)
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
    const_incr = constant_increment(data, 0.5)
    plot_kmeans(const_incr)
    mod_const_incr = constant_increment(data, 0.5)
    plot_kmeans(mod_const_incr)


if __name__ == '__main__':
    main()
