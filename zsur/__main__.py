#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main file to test the whole project"""

import logging
from zsur import readfile
from matplotlib import pyplot as plt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__all__ = ('main',)  # list of public objects of module


def rf():
    try:
        data = readfile('data.txt')  # run with command line
    except FileNotFoundError:
        data = readfile('../data.txt')  # run directly __main__.py
    return data


def plot_data(data: list):
    x, y = zip(*data)
    plt.scatter(x, y, color='black', marker='o')
    plt.show()


def main():
    data = rf()
    plot_data(data)  # show data


if __name__ == '__main__':
    main()
