#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Metoda nerovnomerneho binarniho deleni pro rozdeleni dat do predem znameho poctu trid"""


def main():
    # from main_app import readfile
    # data = readfile('data.txt')
    from zsur.kmeans import kmeans, plot_kmeans
    data = [(-3, 0), (3, 2), (-2, 0), (3, 3), (2, 2), (3, -2), (4, -2), (3, -3)]
    dist = kmeans(data, 2)
    while len(dist) != len(data):
        pass
    plot_kmeans(dist)


if __name__ == '__main__':
    main()
