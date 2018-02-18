from math import sqrt
from random import randint

import matplotlib.pyplot as plt


def distances(points):
    dist = []
    for i in range(len(points) - 1):
        dist.append(sqrt((points[i][0] - points[i+1][0]) ** 2 +
                         (points[i][1] - points[i+1][1]) ** 2))
    return dist


def distance_sort(data, point):
    """
    Sorts points by distance in a way the algorithm needs it. This actually makes the chain map.

    :param data: list of tuples where tuple is one point (x, y,...)
    :param point: starting point
    :return: sorted list of points
    """
    sorted_by_distance = [
        point]  # ok, my point is the first in sorted list (distance is 0)
    points = list(data)  # duplicate data and let's call them 'points'
    while len(points) > 1:  # while points has at least two elements inside, 'point' and one to compare to
        points.remove(point)  # remove sorted point from points
        # sort rest of the points by eucledian distance from the last point in sorted, i don't need sqrt here
        points.sort(key=lambda p: (p[0] - point[0])
                    ** 2 + (p[1] - point[1]) ** 2)
        # get the closest one and append to sorted
        sorted_by_distance.append(points[0])
        point = points[0]  # the new point to sort by eucledian dist from
    return sorted_by_distance  # sorted points


def chain_map(data, iterations, bound):
    """
    Does and plots Chain map alogrithm

    :param iterations: How many times do you want to run the algorithm
    :param data: Entry data in clasic format used in a whole program
    :param bound: Size of a 'jump' from which a new class is recognized
    :return: printed number of classes and two graphs (one with the chain, the other one shows 'jump' lengths)
    """
    d1, d2 = zip(*data)  # unzip data
    for i in range(0, iterations):  # several iterations
        plt.figure(i + 1)  # make new figure
        plt.plot(d1, d2, 'ro')  # plot points to new figure
        rand = randint(0, len(data) - 1)  # select random starting point
        # sorts data by distance, see func docs for more info
        points = distance_sort(data, data[rand])
        for j in range(len(data) - 1):
            p1, p2 = points[j], points[j + 1]
            plt.plot((p1[0], p2[0]), (p1[1], p2[1]), 'b')
        dists = distances(points)
        pocet_trid = len([i for i in dists if i >= bound]) + 1
        print('Metodou retezove mapy byly nalezeny: {} tridy'.format(pocet_trid))
        plt.figure(i + iterations + 1)
        plt.plot([i for i in range(len(dists))], [
                 bound for _ in range(len(dists))])
        plt.plot(dists)
    plt.show()


def main():
    from main import readfile
    data = readfile('../data.txt')
    # data = [(-3, 0), (3, 2), (-2, 0), (3, 3), (2, 2), (3, -2), (4, -2), (3, -3)]
    chain_map(data, 1, 9)


if __name__ == '__main__':
    main()
