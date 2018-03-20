#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main file to test the whole project"""

from zsur.readfile import readfile
from zsur.chain_map import chain_map, plot_chainmap
from zsur.cluster_levels import cluster_levels, print_clusterlvls


__all__ = ('main',)  # list of public objects of module


def rf():
    try:
        data = readfile('data.txt')  # run with command line
    except FileNotFoundError:
        data = readfile('../data.txt')  # run directly __main__.py
    return data


def main():
    data = rf()
    # 1b - just add data, number of iterations to do and boundary to find number of classes from
    chmap = chain_map(data, 9)
    plot_chainmap(chmap)

    lvls = cluster_levels(data, 1.9)
    print_clusterlvls(lvls)


if __name__ == '__main__':
    main()
