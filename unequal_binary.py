def main():
    # from main_app import readfile
    # data = readfile('data.txt')
    # d1, d2 = data['c1'], data['c2']
    # data = list(zip(d1, d2))
    from k_means import k_means, plot_kmeans
    data = [(-3, 0), (3, 2), (-2, 0), (3, 3), (2, 2), (3, -2), (4, -2), (3, -3)]
    dist = k_means(data, 2)
    while len(dist) != len(data):
        pass
    plot_kmeans(dist)


if __name__ == '__main__':
    main()
