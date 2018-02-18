#!/usr/bin/env python

"""genpoints.py: Skript pro generovani bodu ve 2D prostoru"""

import matplotlib.pyplot as plt


def generate_points(start, end, step):
    data = list()
    for i in range(start, end, step):
        for j in range(start, end, step):
            point = (i, j)
            data.append(point)
    return data


def main():
    data = generate_points(-20, 20, 1)
    x, y = zip(*data)
    plt.scatter(x, y)
    plt.show()


if __name__ == '__main__':
    main()
