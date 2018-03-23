#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Klasifikator s linearnimi diskriminacnimi funkcemi

* Rossenblattuv algoritmus
* metoda konstantnich prirustku
* upravena metoda konstantnich prirustku
"""

from zsur.genpoints import generate_points
from zsur.readfile import readfile
from zsur.kmeans import kmeans, plot_kmeans
import numpy as np


def get_lines_ross(data: dict):
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
                        lines[key] = np.transpose(lines[key]) + (x * q)
                        cont = True
    lines = {k: tuple(v) for k, v in lines.items()}
    return lines


def classify_ross(lines, trypoints):
    classified = dict.fromkeys(lines)
    for point in trypoints:
        sides = dict.fromkeys(lines)
        for key, val in lines.items():
            sides[key] = val[0] * point[0] + val[1] * point[1] + val[2]
        keys = [k for k, v in sides.items() if v > 1]
        if len(keys) > 1:
            continue
        else:
            k = keys[0]
            if classified[k] is None:
                classified[k] = [point]
            else:
                classified[k].append(point)
    return classified


def rossenblatt(data, classes, space_size=(-20, 20), step=1):
    data = kmeans(data, classes)
    lines = get_lines_ross(data)
    trypoints = generate_points(space_size[0], space_size[1], step)
    classified = classify_ross(lines, trypoints)
    data = data.update(classified)
    return data


def main():
    data = readfile('../data.txt')
    ross = rossenblatt(data, 3)
    plot_kmeans(ross)


if __name__ == '__main__':
    main()
