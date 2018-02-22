#!/usr/bin/env python

"""nearest_neighbour.py: Klasifikator podle nejblizsiho a dvou nejblizsich sousedu"""

from zsur.k_means import k_means, plot_kmeans
from zsur.cluster_levels import distanc
from zsur.genpoints import generate_points
import itertools


def nearest_neighbour(data, classes, space_size=(-20, 20), step=1):
    kmeans = k_means(data, classes)
    trypoints = generate_points(space_size[0], space_size[1], step)
    points_in_kmeans = list(itertools.chain(*kmeans.values()))
    kmeans_toplot = dict(kmeans)
    for trypoint in trypoints:
        sorted_means = sorted(points_in_kmeans, key=lambda p: distanc(trypoint, p))
        for key, value in kmeans.items():
            for val in value:
                if val == sorted_means[0]:
                    kmeans_toplot[key].append(trypoint)
    plot_kmeans(kmeans_toplot)


def main():
    from main import readfile
    data = readfile('../data.txt')
    nearest_neighbour(data, 3)


if __name__ == '__main__':
    main()
