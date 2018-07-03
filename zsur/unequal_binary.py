#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Metoda nerovnomerneho binarniho deleni pro rozdeleni dat do predem znameho poctu trid"""

import logging
from typing import List
from zsur.kmeans import kmeans, plot_kmeans, criterion
from zsur.readfile import readfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def unequal_binary(data: List[tuple]):
    dist = kmeans(data, 2)  # 1st split to two
    # plot_kmeans(dist)  # inter step
    logging.info('First split')
    crits = criterion(dist)
    max_key = max(crits, key=crits.get)  # take bigger value
    dist2 = kmeans(dist.pop(max_key), 2)  # 2nd split to two
    logging.info('Second split')
    return {**dist, **dist2}  # combine dicts


def main():
    # data = [(-3, 0), (3, 2), (-2, 0), (3, 3), (2, 2), (3, -2), (4, -2), (3, -3)]
    data = readfile('../data.txt')
    dist = unequal_binary(data)
    plot_kmeans(dist)


if __name__ == '__main__':
    main()
