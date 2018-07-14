#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automaticke urceni poctu trid v datech metodou shlukove hladiny"""

import datetime as dt
from zsur.readfile import readfile


def distanc(*args):
    """
    Calcs squared euclidean distance between two points represented by n dimensional vector

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
    size = len(data)
    matrix = {key: list() for key in range(size)}
    for i in range(size):
        for j in range(i, size):
            matrix[j].append(distanc(data[i], data[j]))
    return matrix


def matrix_min(matrix):
    minimums = []
    for val in matrix.values():
        filtered = list(filter(lambda a: a != 0, val))
        if not filtered:
            continue
        else:
            minimums.append(min(filtered))
    minimin = min(minimums)
    for key, val in matrix.items():
        if minimin in val:
            index = val.index(minimin)
            return minimin, key, index


def reconstruct(matrix, i):
    size = len(matrix)
    if len(matrix[i]) == size:
        data1 = matrix[i]
    else:
        data1 = matrix[i][:-1]
        for val in matrix.values():
            append = data1.append
            if len(val) > i:
                append(val[i])
    return data1


def restruct(matrix, row, datamin):
    rowsize = len(matrix[row])
    matrix[row] = datamin[:rowsize]
    for i in range(len(datamin) - rowsize + 1):
        matrix[i + row][row] = datamin[i + rowsize - 1]
    return matrix


def removal(matrix, column):
    matrix.pop(column)
    for key, val in matrix.items():
        if len(val) > column:
            del val[column]
    return matrix


def reduce_matrix(matrix, row, column):
    """
    Function with side effect!

    :param dict matrix:
    :param row:
    :param column:
    :return:
    """
    if row > column:
        row, column = column, row
    data1 = reconstruct(matrix, row)
    data2 = reconstruct(matrix, column)
    datamin = [min(i) for i in zip(data1, data2)]
    matrix = restruct(matrix, row, datamin)
    matrix = removal(matrix, column)
    legn = len(matrix)
    for i in range(column, legn):
        matrix[i] = matrix.pop(i + 1)
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
    """
    Does aglomerative algorithm, I used control prints here, to know how long it takes to generate matrix,
    how long it takes to reduce matrix and finally to know how many classes is in dataset, but I suppose, that I can
    find it on github...
    https://github.com/mareklovci/zsur/blob/6eaba2de4b15933412a6da7b28efc329617b4111/zsur/cluster_levels.py

    :param list data: entry data
    :param float boundary: size of a 'jump' from which a new class is recognized (aka 'magic constant')
    :return: number of classes in dataset
    """
    data = [(int(round(i)), int(round(j))) for i, j in data]
    t0 = dt.datetime.now()
    matrix = generate_matrix(data)
    t1 = dt.datetime.now()
    print('cas', t1 - t0)
    minimums = []
    for i in range(len(matrix) - 1):
        minimums.append(matrix_min(matrix))
        matrix = reduce_matrix(matrix, minimums[i][1], minimums[i][2])
    return classes(minimums, boundary)


def print_clusterlvls(clas):
    print('\nAglomerativni metodou byly nalezeny: {} tridy'.format(clas))


def main():
    data = readfile('data.txt')
    # data = [(-3, 1), (1, 1), (-2, 0), (3, -3), (1, 2), (-2, -1)]
    t0 = dt.datetime.now()
    lvls = cluster_levels(data, 1.9)
    t1 = dt.datetime.now()
    print('cas', t1 - t0)
    print_clusterlvls(lvls)


if __name__ == '__main__':
    main()
