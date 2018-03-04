#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main file to test the whole project"""

from zsur.chain_map import chain_map, plot_chainmap
from zsur.cluster_levels import cluster_levels, print_clusterlvls


def readfile(infile):
    """
    Read data from file

    :param infile: file with lines in format 'float float'
    :return: list of tuples, tuple = point(x, y)
    """
    data = list()
    with open(infile, 'rt') as f:
        for line in f:
            v1, v2 = line.split()
            data.append((float(v1), float(v2)))
    return data


def main():
    data = readfile('data.txt')
    # 1b - just add data, number of iterations to do and boundary to find number of classes from
    chmap = chain_map(data, 9)
    plot_chainmap(chmap)

    lvls = cluster_levels(data, 1.9)
    print_clusterlvls(lvls)


if __name__ == '__main__':
    main()
