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
    dist = dict(dist)
    changed = True
    while changed:
        changed = False
        for key, val in dist.items():
            for item in val:
                if len(val) == 1:
                    break
                min_a2 = (-1, (None, None), (None, None))  # (value, new_center, old_center)
                a1 = a_criterions(item, key, len(val), len(val) - 1)
                used_keys = [key]
                for k in _get_unused_key(dist, used_keys):
                    used_keys.append(k)
                    a2 = a_criterions(item, k, len(val), len(val) + 1)
                    if min_a2[0] == -1 or a2 < min_a2[0]:
                        min_a2 = (a2, k, key)
                if a1 > min_a2[0] != -1:
                    changed = True
                    dist = _move_point(dist, item, min_a2[2], min_a2[1])
                    dist = _actualize_keys(dist)
                    break
            if changed:
                break
    return dist


def _actualize_keys(data: Dict[tuple, List[tuple]]):
    logging.info('Actualizing keys')
    dist = dict(data)
    for key, val in dist.items():
        new_key = [sum(x) for x in zip(*val)]
        new_key = [i/len(dist[key]) for i in new_key]
        new_key = tuple(new_key)
        if new_key not in dist:
            dist[new_key] = dist[key]
            del dist[key]
    return dist


def _move_point(dist: Dict[Tuple[float], List[Tuple[float]]], point_to_move: tuple, orig_key, key_where_to_move: tuple):
    dist = dict(dist)
    logging.info('Moving {} from key {} to key {}'.format(point_to_move, orig_key, key_where_to_move))
    logging.info('Current keys in dict {}'.format([key for key in dist.keys()]))
    index_of_point: int = dist[orig_key].index(point_to_move)
    point: tuple = dist[orig_key].pop(index_of_point)
    dist[key_where_to_move].append(point)
    return dist


def _get_unused_key(dist: dict, used_keys):
    for key in dist.keys():
        if key not in used_keys:
            yield key


def plot_kmeans(dist):
    for key, value in dist.items():
        x, y = zip(*value)
        plt.scatter(x, y)
        plt.plot(key[0], key[1], color='black', marker='o')
    plt.show()


def a_criterions(x: tuple, center: tuple, old_len, new_len):
    """(s(k)/(s(k)-1))*d^2[x, c(k)]"""
    first = old_len/new_len
    second = (x[0] - center[0])**2 + (x[1] - center[1])**2
    a = first * second
    return a


def shuffle_dict(dist, no: int = 20):
    dist = dict(dist)
    for key, val in dist.items():
        used_keys = [key]
        items = [val[i] for i in range(no)]
        count = 0
        for k in _get_unused_key(dist, used_keys):
            used_keys.append(k)
            for _ in range(10):
                dist[k].append(items[count])
                count += 1
    return dist


def main():
    data = readfile('../data.txt')
    # kmeans
    dist = kmeans(data, 3)
    crits = criterion(dist)
    logging.info('Values of criterial function: {}'.format(crits))
    plot_kmeans(dist)
    # shuffle some points
    dist = shuffle_dict(dist)
    plot_kmeans(dist)
    # fix shuffle
    optimalised = iterative_optimization(dist)
    plot_kmeans(optimalised)


if __name__ == '__main__':
    main()
