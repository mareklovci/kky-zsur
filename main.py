from zsur.chain_map import chain_map
from zsur.cluster_levels import cluster_levels


def readfile(infile):
    """
    Read data from file

    :param infile: file in format 'float float'
    :return: list of tuples, tuple = point(x, y)
    """
    data = {'c1': [], 'c2': []}
    with open(infile, 'rt') as f:
        for line in f:
            v1, v2 = line.split()
            data['c1'].append(float(v1))
            data['c2'].append(float(v2))
    d1, d2 = data['c1'], data['c2']
    data = list(zip(d1, d2))
    return data


def main():
    data = readfile('data.txt')
    # 1b - just add data, number of iterations to do and boundary to find number of classes from
    chain_map(data, 1, 9)
    cluster_levels(data, 1.9)


if __name__ == '__main__':
    main()
