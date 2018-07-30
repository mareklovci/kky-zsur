#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Main file to test the whole project"""

import logging
from zsur.readfile import readfile
from matplotlib import pyplot as plt
from zsur.bayes import main as bayes
from zsur.chain_map import main as chmap
from zsur.cluster_levels import main as cluster
from zsur.kmeans import main as kmeans
from zsur.linear_disc import main as lindisc
from zsur.maximin import main as maximin
from zsur.minimal_distance import main as mindist
from zsur.nearest_neighbour import main as nearneigh
from zsur.unequal_binary import main as unebin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

__all__ = ('main',)  # list of public objects of module


def plot_data(data: list):
    x, y = zip(*data)
    plt.scatter(x, y, color='black', marker='o')
    plt.show()


def main():
    data = readfile('data.txt')
    plot_data(data)  # show data
    # metoda shlukove hladiny
    logging.info('metoda shlukove hladiny')
    cluster()
    # metoda retezove mapy
    logging.info('metoda retezove mapy')
    chmap()
    # metoda maximin
    logging.info('metoda maximin')
    maximin()
    # nerovnomerne binarni deleni
    logging.info('nerovnomerne binarni deleni')
    unebin()
    # kmeans
    logging.info('kmeans')
    kmeans()
    # bayesuv klasifikator
    logging.info('bayesuv klasifikator')
    bayes()
    # klasifikator podle minimalni vzdalenosti
    logging.info('klasifikator podle minimalni vzdalenosti')
    mindist()
    # klasifikator podle k-nejblizsiho souseda
    logging.info('klasifikator podle k-nejblizsiho souseda')
    nearneigh()
    # klasifikator s linearnimi diskriminacnimi funkcemi
    logging.info('klasifikator s linearnimi diskriminacnimi funkcemi')
    lindisc()


if __name__ == '__main__':
    main()
