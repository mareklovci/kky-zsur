#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automaticke urceni poctu trid v datech metodou retezove mapy"""

from math import sqrt
from random import choice
from zsur.cluster_levels import distanc
from zsur.readfile import readfile
import matplotlib.pyplot as plt


def distances(points):
    """
    Makes list of distances from point to point.

    :param list points: list of points to get distances from
    :return: list of distances from point to point
    """
    dist = [sqrt(distanc(points[i], points[i+1])) for i in range(len(points) - 1)]
    return dist


def distance_sort(data, point):
    """
    Sorts points by distance in a way the algorithm needs it. This actually makes the chain map.

    :param list data: list of tuples where tuple is one point (x, y,...)
    :param tuple point: starting point
    :return: sorted list of points
    """
    sorted_by_distance = [point]  # ok, my point is the first in sorted list (distance is 0)
    points = data.copy()  # duplicate data and let's call them 'points'
    while len(points) > 1:  # while points has at least two elements inside, 'point' and one to compare to
        points.remove(point)  # remove sorted point from points
        # sort rest of the points by eucledian distance from the last point in sorted, i don't need sqrt here
        points.sort(key=lambda p: distanc(p, point))
        sorted_by_distance.append(points[0])  # get the closest one and append to sorted
        point = points[0]  # the new point to sort by eucledian dist from
    return sorted_by_distance  # sorted points


def chain_map(data, bound):
    """
    Chain map alogrithm

    :param list data: entry data in clasic format used in a whole program
    :param float bound: size of a 'jump' from which a new class is recognized
    :return: sorted points, list of distances from point to point, number of classes in data
    """
    rand = choice(data)  # select random starting point
    points = distance_sort(data, rand)  # sort data by distance, see func docs for more info
    dists = distances(points)
    # alternative to code below: len([i for i in dists if i >= bound]) + 1
    pocet_trid = len(list(filter(lambda x: x >= bound, dists))) + 1
    return points, dists, pocet_trid, bound


def plot_chainmap(inpt):
    """
    Plots chain map algorithm - makes two graphs and one print()

    :param tuple inpt: (points, dists, pocet_trid, bound) - output from chain_map()
    :return: printed number of classes and two graphs (one with the chain, the other one shows 'jump' lengths)
    """
    points, dists, pocet_trid, bound = inpt
    d1, d2 = zip(*points)  # unzip data
    plt.figure()  # make new figure
    plt.plot(d1, d2, 'ro')  # plot points to new figure
    for j in range(len(points) - 1):
        p1, p2 = points[j], points[j + 1]
        plt.plot((p1[0], p2[0]),
                 (p1[1], p2[1]), 'b')
    print('Metodou retezove mapy byly nalezeny: {} tridy'.format(pocet_trid))
    plt.figure()
    plt.plot([i for i in range(len(dists))],
             [bound for _ in range(len(dists))])
    plt.plot(dists)
    plt.show()


def main():
    data = readfile('../data.txt')
    chmap = chain_map(data, 9)
    plot_chainmap(chmap)


if __name__ == '__main__':
    main()
