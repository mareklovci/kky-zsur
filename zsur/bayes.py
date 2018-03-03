#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bayesuv klasifikator"""

from zsur.kmeans import kmeans


def main():
    from main import readfile
    data = readfile('../data.txt')
    dist = kmeans(data, 3)
    print(dist)


if __name__ == '__main__':
    main()
