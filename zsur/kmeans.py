#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Algoritmus k-means pro rozdeleni dat do predem znameho poctu trid"""

from random import choice
from zsur.maximin import distances_to_centers
from zsur.cluster_levels import distanc
import matplotlib.pyplot as plt


def getcenter(data, r):
    """
    Generator of 'r' random centers, generated from 'data'. Why is this generator? Why not...
    # TODO: misto 'r' nahodnych stredu vem 'r' od sebe nejvzdalenejsich

    :param data: data to generate centers from
    :param int r: how many centers to generate
    :return: generator of points -> tuple(x, y)
    """
    chosen = set()  # already chosen points
    i = 0
    while i < r:
        point = choice(data)  # choose point
        if point not in chosen:
            yield point
            i += 1
        else:  # if point was already chosen, choose the other one
            continue


def sort_to_classes(distances, minlist):
    for minimum in minlist:
        for value in distances.values():
            mini = value.get(minimum[0])
            if mini != minimum[1]:
                del value[minimum[0]]
    return distances


def get_new_centers(distances):
    noi = {key: len(val.values()) for key, val in distances.items()}  # dict -> key: how many items is in each class
    newcenters = {}
    for key, value in distances.items():
        newpoint = (0, 0)
        for k in value.keys():
            newpoint = tuple(map(lambda x, y: x + y, newpoint, k))
        newpoint = tuple(map(lambda x: x / noi[key], newpoint))
        newcenters[newpoint] = {}
    return newcenters


def criterion(dist):
    """
    Computes criterial values for each center in dict(dist). Computes how far is it from each point in data (additional
    argument) to every center in dist. Chooses minimal distance for each point and sums those minimums for every center.
    Next usage: iterative optimization.
    !!! That is how we did it on the paper. I had to use different approach.
    I did not computed distance from each point in dataset, but I used points already assigned to class. It is much
    easier to programm.

    :param dict dist: dict from kmeans
    :return: criterial values for each center (J values)
    """
    distances = dict.fromkeys(dist)
    for key, val in dist.items():
        distances[key] = {point: distanc(key, point) for point in val}
    crits = {key: int(sum(val.values())) for key, val in distances.items()}
    return crits


def kmeans(data, r):
    distances = dict((c, {}) for c in getcenter(data, r))
    while True:
        distances = distances_to_centers(distances, data)
        minlist = []
        for value in zip(*(val.items() for val in distances.values())):
            minlist.append(min(value))
        sort_to_classes(distances, minlist)
        newcenters = get_new_centers(distances)
        if newcenters.keys() == distances.keys():
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
    dist = kmeans(data, 3)
    crits = criterion(dist)
    print(crits)
    plot_kmeans(dist)


if __name__ == '__main__':
    main()
