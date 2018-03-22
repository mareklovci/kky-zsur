#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Klasifikator s linearnimi diskriminacnimi funkcemi

* Rossenblattuv algoritmus
* metoda konstantnich prirustku
* upravena metoda konstantnich prirustku
"""

from zsur.genpoints import generate_points
from zsur.readfile import readfile
from zsur.kmeans import kmeans
import numpy as np


def rossenblatt(data, classes):
    data = kmeans(data, classes)
    lines = dict().fromkeys(data, [1, 1, 1])  # vyhrazeni prostoru pro koeficienty primek
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


def plot_ross(data):
    pass


def main():
    data = readfile('../data.txt')
    ross = rossenblatt(data, 3)
    print(ross)


if __name__ == '__main__':
    main()
