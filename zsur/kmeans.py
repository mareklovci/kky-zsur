#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Algoritmus k-means pro rozdeleni dat do predem znameho poctu trid"""

import logging
from random import choice
from zsur import distances_to_centers, distanc, readfile
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def get_criterial_function_minimum(dist: Dict[Tuple[float], List[Tuple[float]]]):
    crit = criterion(dist)
    min_key = min(crit, key=crit.get)
    return crit[min_key]


def update_list_dict(d: dict, key, value):
    """Side effect function!"""
    if d[key] is None:
        d[key] = [value]
    else:
        d[key].append(value)


def kmeans(data: List[tuple], r):
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
            update_list_dict(points, key, k)
    return points


def iterative_optimization(dist: Dict[Tuple[float], List[Tuple[float]]]):
    for key, val in dist.items():
        while len(val) > 1:  # cannot destroy one-value set
            j = get_criterial_function_minimum(dist)
            point = val.pop()
            for new_key in _get_unused_key(dist, key):
                _move_point(dist, point, new_key)
                new_j = get_criterial_function_minimum(dist)
                if j <= new_j:
                    _move_point(dist, point, key)
                else:
                    _actualize_keys()
        k = _get_unused_key(dist, key)
        print(k)


def _actualize_keys():
    pass


def _move_point(dist: Dict[Tuple[float], List[Tuple[float]]], point_to_move: tuple, key_where_to_move: tuple):
    dist[key_where_to_move].append(point_to_move)


def _get_unused_key(dist: dict, current_key):
    for key in dist.keys():
        if key == current_key:
            pass
        else:
            yield key


def plot_kmeans(dist):
    for key, value in dist.items():
        x, y = zip(*value)
        plt.scatter(x, y)
        plt.plot(key[0], key[1], color='black', marker='o')
    plt.show()


def main():
    data = readfile('../data.txt')
    dist = kmeans(data, 3)
    crits = criterion(dist)
    logging.info('Values of criterial function: {}'.format(crits))
    plot_kmeans(dist)
    iterative_optimization(dist)


if __name__ == '__main__':
    main()
