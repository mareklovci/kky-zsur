#!/usr/bin/env python

"""minimal_distance.py: Klasifikator podle minimalni vzdalenosti"""

from zsur.k_means import k_means, plot_kmeans
from zsur.cluster_levels import distanc
from zsur.genpoints import generate_points


def minimal_distance(data, classes, space_size=(-20, 20), step=1):
    dist = k_means(data, classes)
    trypoints = generate_points(space_size[0], space_size[1], step)
    for point in trypoints:
        distances = {}
        for k in dist.keys():
            distances[k] = distanc(point, k)
        key_of_min = min(distances.keys(), key=(lambda key: distances[key]))
        dist[key_of_min].append(point)
    plot_kmeans(dist)


def main():
    from main import readfile
    data = readfile('../data.txt')
    minimal_distance(data, 3)


if __name__ == '__main__':
    main()
