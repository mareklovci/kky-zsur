#!/usr/bin/env python

"""bayes.py: Bayesuv klasifikator"""

from k_means import k_means


def main():
    from main_app import readfile
    data = readfile('data.txt')
    dist = k_means(data, 3)
    print(dist)


if __name__ == '__main__':
    main()
