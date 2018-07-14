#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automaticke urceni poctu trid v datech metodou shlukove hladiny"""

import logging
import numpy as np
from zsur.readfile import readfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def distanc(*args):
    """Calcs squared euclidean distance between two points represented by n dimensional vector

    :param tuple args: points to calc distance from
    :return: euclidean distance of points in *args
    """
    if len(args) == 1:
        raise Exception('Not enough input arguments (expected two)')
    if len(args) > 2:
        raise Exception('Too many input arguments (expected two)')
    else:
        vec1, vec2 = args
    if len(vec1) != len(vec2):
        raise Exception('Input vectors have to have same length')
    else:
        return sum((a - b) ** 2 for a, b in zip(vec1, vec2))


def generate_matrix(data):
    logging.info('Generating matrix from data')
    size = len(data)
    matrix = np.zeros((size, size), dtype=np.float)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            matrix[j, i] = distanc(data[i], data[j])
            matrix[i, j] = matrix[j, i]
    logging.info('Matrix generating finished')
    return matrix


def matrix_min(matrix):
    minimum = np.min(matrix[np.nonzero(matrix)])
    index1, index2 = np.where(matrix == minimum)
    if len(index1) >= 2:
        return minimum, index2[0], index2[1]
    else:
        return minimum, index1[0], index2[0]


def reduce_matrix(matrix, row, column):
    logging.info('Reducing matrix - size {}'.format(len(matrix)))
    for i in range(len(matrix)):
        if matrix[row, i] > matrix[column, i]:
            matrix[i, row] = matrix[i, column]
        else:
            matrix[i, column] = matrix[i, row]
    matrix = np.delete(matrix, column, 1)
    matrix = np.delete(matrix, column, 0)
    return matrix


def reduce_matrix2(matrix, row, column):
    """Function with side effect!

    :param matrix:
    :param row:
    :param column:
    :return:
    """
    for i in range(len(matrix)):
        if matrix[row, i] > matrix[column, i]:
            matrix[i, row] = matrix[i, column]
        else:
            matrix[i, column] = matrix[i, row]
    matrix[column, :] = 0
    matrix[:, column] = 0
    return matrix


def classes(minimums, boundary):
    clas = 0
    rev = list(reversed(minimums))
    for i in range(len(minimums)):
        if rev[i][0] / boundary >= rev[i + 1][0]:
            clas += 1
        else:
            break
    return clas


def cluster_levels(data, boundary):
    """Does aglomerative algorithm

    :param list data: entry data
    :param float boundary: size of a 'jump' from which a new class is recognized (aka 'magic constant')
    :return: number of classes in dataset
    """
    matrix = generate_matrix(data)
    minimums = []
    for i in range(len(matrix) - 1):
        minimums.append(matrix_min(matrix))
        matrix = reduce_matrix(matrix, minimums[i][1], minimums[i][2])
    return classes(minimums, boundary)


def main():
    data = readfile('data.txt')
    lvls = cluster_levels(data, 1.9)
    logger.info('Aglomerativni metodou byly nalezeny: {} tridy'.format(lvls))


if __name__ == '__main__':
    main()
