#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automaticke urceni poctu trid v datech metodou shlukove hladiny"""

import numpy as np


def distanc(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def generate_matrix(data):
    size = len(data)
    matrix = np.zeros((size, size), dtype=np.float)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            matrix[j, i] = distanc(data[i], data[j])
            matrix[i, j] = matrix[j, i]
    return matrix


def matrix_min(matrix):
    minimum = np.min(matrix[np.nonzero(matrix)])
    index1, index2 = np.where(matrix == minimum)
    if len(index1) >= 2:
        return minimum, index2[0], index2[1]
    else:
        return minimum, index1[0], index2[0]


def reduce_matrix(matrix, row, column):
    for i in range(len(matrix)):
        if matrix[row, i] > matrix[column, i]:
            matrix[i, row] = matrix[i, column]
        else:
            matrix[i, column] = matrix[i, row]
    matrix = np.delete(matrix, column, 1)
    matrix = np.delete(matrix, column, 0)
    return matrix


def cluster_levels(data, boundary):
    """
    Does aglomerative algorithm, I used control prints here, to know how long it takes to generate matrix,
    how long it takes to reduce matrix and finally to know how many classes is in dataset, but I suppose, that I can
    find it on github...
    https://github.com/mareklovci/zsur/blob/6eaba2de4b15933412a6da7b28efc329617b4111/zsur/cluster_levels.py

    :param list data: entry data
    :param float boundary: size of a 'jump' from which a new class is recognized (aka 'magic constant')
    :return: number of classes in dataset
    """
    matrix = generate_matrix(data)
    minimums = []
    for i in range(len(matrix) - 1):
        minimums.append(matrix_min(matrix))
        matrix = reduce_matrix(matrix, minimums[i][1], minimums[i][2])
    classes = 0
    for i in range(len(minimums)):
        rev = list(reversed(minimums))
        if rev[i][0] / boundary >= rev[i + 1][0]:
            classes += 1
        else:
            break
    return classes


def print_clusterlvls(classes):
    print('\nAglomerativni metodou byly nalezeny: {} tridy'.format(classes))


def main():
    from main import readfile
    data = readfile('../data.txt')
    lvls = cluster_levels(data, 1.9)
    print_clusterlvls(lvls)


if __name__ == '__main__':
    main()
