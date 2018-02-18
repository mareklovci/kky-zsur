#!/usr/bin/env python

"""minimal_distance.py: Klasifikator podle minimalni vzdalenosti"""

from k_means import k_means, plot_kmeans
from cluster_levels import distanc
from genpoints import generate_points


def minimal_distance(data):
    dist = k_means(data, 3)
    trypoints = generate_points(-20, 20, 1)
    for point in trypoints:
        distances = {}
        for k in dist.keys():
            distances[k] = distanc(point, k)
        key_of_min = min(distances.keys(), key=(lambda key: distances[key]))
        dist[key_of_min].append(point)
    plot_kmeans(dist)


def main():
    from main_app import readfile
    data = readfile('data.txt')
    minimal_distance(data)


if __name__ == '__main__':
    main()