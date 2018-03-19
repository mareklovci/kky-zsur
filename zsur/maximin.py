#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automaticke urceni poctu trid v datech metodou MAXIMIN"""

from itertools import combinations
from zsur.cluster_levels import distanc
from zsur.readfile import readfile


def average_center_distance(q, distances):
    distances = [distanc(c[0], c[1]) for c in combinations(distances.keys(), 2)]
    return sum(distances) / len(distances) * q


def distances_to_centers(distances, data):
    """
    For each datum in 'data' gets eucledian distance from self to each key in 'distances' dict().
    This distance is stored in nested dict in format >> distances.keys(): {'all data points': 'dist from point to key'}

    :param dict distances: unspecified dictionary
    :param list data: list of tuples
    :return: nested dict in format >> distances.keys(): {'all data points': 'dist from point to key'}
    """
    centers = dict.fromkeys(distances)
    for center in centers.keys():
        centers[center] = {key: distanc(key, center) for key in data}
    return centers


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
        distances = distances_to_centers(distances, data)
        maxvalue = get_maxmin(distances)
        avg = average_center_distance(q, distances)
        if maxvalue[1] > avg:
            distances[maxvalue[0]] = {}
            data.remove(maxvalue[0])
        else:
            break
    return len(distances.keys())  # return number of clusters


def main():
    data = readfile('../data.txt')
    # data = [(2, -3), (3, 3), (2, 2), (-3, 1), (-1, 0), (-3, -2), (1, -2), (3, 2)]
    no_of_clusters = maximin(data, 0.3)
    print(no_of_clusters)


if __name__ == '__main__':
    main()
