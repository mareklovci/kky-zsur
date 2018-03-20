#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bayesuv klasifikator"""

from zsur.kmeans import kmeans, plot_kmeans
from zsur.readfile import readfile
from zsur.genpoints import generate_points
from scipy.stats import multivariate_normal
import numpy as np


def sigma(data: dict, prumery):
    """
    Function to get covariance matrix

    :param prumery:
    :param dict data: dict with points after kmeans
    :return: kovariancni matice
    """
    sigmy = dict.fromkeys(data)
    for key, value in data.items():
        sigm = np.zeros(2)
        for val in value:
            v1 = np.matrix(np.subtract(val, prumery[key]))
            v2 = np.matrix(np.subtract(val, prumery[key]))
            v3 = v1.T * v2
            sigm = sigm + v3
        sigmy[key] = sigm/len(value)
    return sigmy


def probability(data: dict) -> dict:
    """
    Function to calculate P(omega)

    :param dict data: dict to get data from
    :return:
    """
    counter = {key: len(val) for key, val in data.items()}
    summary = sum(counter.values())
    probabi = {key: val/summary for key, val in counter.items()}
    return probabi


def normal_guess(point, sigm, mean, prob):
    normal = multivariate_normal(mean=mean, cov=sigm)
    return prob * normal.pdf(point)


def is_pos_def(x):
    return np.all(np.linalg.eigvals(x) > 0)


def bayes(data, classes, space_size=(-20, 20), step=1):
    dist = kmeans(data, classes)
    trypoints = generate_points(space_size[0], space_size[1], step)
    prob = probability(dist)
    prumery = dict.fromkeys(dist)
    for key, val in dist.items():
        ls1, ls2 = zip(*val)
        s1, s2 = sum(ls1), sum(ls2)
        prumery[key] = tuple(map(lambda x: x/len(val), (s1, s2)))
    sigm = sigma(dist, prumery)
    for point in trypoints:
        rozhodovaci = {key: normal_guess(point, sigm[key], prumery[key], prob[key]) for key in dist.keys()}
        keywithmaxvalue = max(rozhodovaci, key=rozhodovaci.get)
        dist[keywithmaxvalue].append(point)
    return dist


def main():
    data = readfile('../data.txt')
    baye = bayes(data, 3)
    plot_kmeans(baye)


if __name__ == '__main__':
    main()
