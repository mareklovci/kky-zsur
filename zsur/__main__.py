#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main file to test the whole project"""

from zsur.readfile import readfile
from zsur.chain_map import chain_map, plot_chainmap
from zsur.cluster_levels import cluster_levels, print_clusterlvls


def main():
    try:
        data = readfile('data.txt')
    except FileNotFoundError:
        data = readfile('../data.txt')
    # 1b - just add data, number of iterations to do and boundary to find number of classes from
    chmap = chain_map(data, 9)
    plot_chainmap(chmap)

    lvls = cluster_levels(data, 1.9)
    print_clusterlvls(lvls)


if __name__ == '__main__':
    main()
