#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automaticke urceni poctu trid v datech metodou MAXIMIN"""

from itertools import combinations


def get_distances(data, point):
    result = {}
    for p in data:
        result[p] = get_distance((p, point))
    return result


def get_distance(tupl):
    a, b = tupl[0], tupl[1]
    x, y = a[0] - b[0], a[1] - b[1]
    return x ** 2 + y ** 2


def sort_by_distance(data, point):
    points = list(data)
    points.sort(key=lambda p: (p[0] - point[0]) ** 2 + (p[1] - point[1]) ** 2)
    return points


def average_center_distance(q, distances):
    average_center_distances, combs = [], []
    for comb in combinations(distances.keys(), 2):
        combs.append(comb)
        average_center_distances.append(get_distance(comb))
    return sum(average_center_distances) / len(list(combs)) * q


def maximin(data, q):
    mi1 = data.pop(0)  # get first point
    mi2 = sort_by_distance(data, mi1)[-1]  # mi2 is the furthest point from mi1
    data.remove(mi2)
    distances = {mi1: {}, mi2: {}}
    while True:
        for stred in distances.keys():
            distances[stred] = get_distances(data, stred)
        minlist = []
        for value in zip(*(val.items() for val in distances.values())):
            minlist.append(min(value))
        maxvalue = max(minlist)
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
