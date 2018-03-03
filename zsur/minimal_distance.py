#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Klasifikator podle minimalni vzdalenosti"""

from zsur.k_means import k_means, plot_kmeans
from zsur.cluster_levels import distanc
from zsur.genpoints import generate_points


def minimal_distance(data, classes, space_size=(-20, 20), step=1):
    dist = k_means(data, classes)
    trypoints = generate_points(space_size[0], space_size[1], step)
    for point in trypoints:
        distances = {key: distanc(point, key) for key in dist.keys()}  # dict for each point -> key: distance to him
        key_of_min = min(distances.keys(), key=(lambda key: distances[key]))  # select key with minimum distance
        dist[key_of_min].append(point)  # add point to this key
    return dist


def main():
    from main import readfile
    data = readfile('../data.txt')
    processed_data = minimal_distance(data, 3)
    plot_kmeans(processed_data)


if __name__ == '__main__':
    main()
