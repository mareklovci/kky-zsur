#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main file to test the whole project"""

import logging
from zsur import readfile, chain_map, plot_chainmap, cluster_levels

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info('Aglomerativni metodou byly nalezeny: {} tridy'.format(lvls))


if __name__ == '__main__':
    main()
