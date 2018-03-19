#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bayesuv klasifikator"""

from zsur.kmeans import kmeans
from zsur.readfile import readfile


def sigma(data):
    sigm = 0
    pass


def probability(data):
    """
    Function to calculate P(omega)

    :param dict data: dict to get data from
    :return:
    """
    counter = {key: len(val) for key, val in data.items()}
    summary = sum(counter.values())
    probabi = {key: val/summary for key, val in counter.items()}
    return probabi


def main():
    data = readfile('../data.txt')
    dist = kmeans(data, 3)
    prob = probability(dist)
    print(prob)


if __name__ == '__main__':
    main()
