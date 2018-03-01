#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Algoritmus k-means pro rozdeleni dat do predem znameho poctu trid"""

from random import randint
from zsur.maximin import get_distances
import matplotlib.pyplot as plt


def get_centers(data, r):
    # TODO: misto r nahodnych stredu vem r od sebe nejvzdalenejsich
    stredy = []
    for i in range(r):
        point = data[randint(0, len(data) - 1)]
        stredy.append(point)
    return stredy


def sort_to_classes(distances, minlist):
    for minimum in minlist:
        for value in distances.values():
            mini = value.get(minimum[0])
            if mini != minimum[1]:
                del value[minimum[0]]
    return distances


def get_criterions(distances):
    criterions = dict.fromkeys(distances, 0)
    for key, val in distances.items():
        for value in val.values():
            criterions[key] += value
    return criterions


def nos_of_items_in_classes(distances):
    lengths = dict.fromkeys(distances, 0)
    for key, value in distances.items():
        lengths[key] = len(value.values())
    return lengths


def get_new_centers(distances):
    noi = nos_of_items_in_classes(distances)
    newcenters = {}
    for key, value in distances.items():
        newpoint = (0, 0)
        for k in value.keys():
            newpoint = tuple(map(lambda x, y: x + y, newpoint, k))
        newpoint = tuple(map(lambda x: x / noi[key], newpoint))
        newcenters[newpoint] = {}
    return newcenters


def k_means(data, r):
    distances = dict((center, {}) for center in get_centers(data, r))
    while True:
        for center in distances.keys():
            distances[center] = get_distances(data, center)
        minlist = []
        for value in zip(*(val.items() for val in distances.values())):
            minlist.append(min(value))
        sort_to_classes(distances, minlist)
        newcenters = get_new_centers(distances)
        if newcenters.keys() == distances.keys():
            # print(get_criterions(distances))
            break
        else:
            distances = newcenters
    points = dict.fromkeys(distances)
    for key, value in distances.items():
        for k in value.keys():
            if points[key] is None:
                points[key] = [k]
            else:
                points[key].append(k)
    return points


def plot_kmeans(dist):
    for key, value in dist.items():
        x, y = zip(*value)
        plt.scatter(x, y)
        plt.plot(key[0], key[1], color='black', marker='o')
    plt.show()


def main():
    from main import readfile
    data = readfile('../data.txt')
    # data = [(0, 1), (2, 1), (1, 3), (1, -1), (1, 5), (1, 9), (-1, 7), (3, 7)]
    dist = k_means(data, 3)
    plot_kmeans(dist)


if __name__ == '__main__':
    main()
