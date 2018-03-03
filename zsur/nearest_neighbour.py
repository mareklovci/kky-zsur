#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Klasifikator podle nejblizsiho a dvou nejblizsich sousedu"""

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
    return kmeans_toplot


def average_dist(bod, points):
    distances = [distanc(point, bod) for point in points]
    return sum(distances)/len(points)


def knearest_neighbour(data, classes, space_size=(-20, 20), step=1):
    kmeans = k_means(data, classes)
    trypoints = generate_points(space_size[0], space_size[1], step)
    means_toplot = dict(kmeans)
    for trypoint in trypoints:
        for val in kmeans.values():
            val.sort(key=lambda p: distanc(trypoint, p))
        newdict = {key: average_dist(trypoint, kmeans[key]) for key in kmeans.keys()}
        keywithminvalue = min(newdict, key=newdict.get)
        means_toplot[keywithminvalue].append(trypoint)
    return means_toplot


def main():
    from main import readfile
    data = readfile('../data.txt')
    processed_data1 = nearest_neighbour(data, 3)
    processed_data2 = knearest_neighbour(data, 3)
    plot_kmeans(processed_data1)
    plot_kmeans(processed_data2)


if __name__ == '__main__':
    main()
