#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automaticke urceni poctu trid v datech metodou MAXIMIN"""

from itertools import combinations
from zsur.cluster_levels import distanc


def average_center_distance(q, distances):
    distances = [distanc(c[0], c[1]) for c in combinations(distances.keys(), 2)]
    return sum(distances) / len(distances) * q


def vzdalenosti(distances, data):
    distances = distances.copy()
    for stred in distances.keys():
        distances[stred] = {key: distanc(key, stred) for key in data}
    return distances


def get_maxmin(distances):
    minlist = []
    for value in zip(*(val.items() for val in distances.values())):
        minlist.append(min(value))
    return max(minlist)


def maximin(data, q):
    data = data.copy()  # copy data, just to be sure I will not screw something up
    mi1 = data.pop(0)  # get first point
    # mi2 is the furthest point from mi1
    mi2 = sorted(data, key=lambda p: distanc(p, mi1))[-1]  # sort data by distance from mi1 and get the last element
    data.remove(mi2)
    distances = {mi1: {}, mi2: {}}
    while True:
        distances = vzdalenosti(distances, data)
        maxvalue = get_maxmin(distances)
        avg = average_center_distance(q, distances)
        if maxvalue[1] > avg:
            distances[maxvalue[0]] = {}
            data.remove(maxvalue[0])
        else:
            break
    return len(distances.keys())  # return number of clusters


def main():
    from main import readfile
    data = readfile('../data.txt')
    # data = [(2, -3), (3, 3), (2, 2), (-3, 1), (-1, 0), (-3, -2), (1, -2), (3, 2)]
    no_of_clusters = maximin(data, 0.3)
    print(no_of_clusters)


if __name__ == '__main__':
    main()
