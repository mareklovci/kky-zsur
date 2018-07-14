def rf(infile):
    data = list()
    with open(infile, 'rt') as f:
        for line in f:
            v1, v2 = line.split()
            data.append((float(v1), float(v2)))
    return data


def readfile(infile: str):
    """Read data from file

    :param infile: file with lines in format 'float float'
    :return: list of tuples, tuple = point(x, y)
    """
    try:
        data = rf(infile)  # run with command line
    except FileNotFoundError:
        data = rf('../' + infile)  # run directly __main__.py
    return data


def main():
    pass


if __name__ == '__main__':
    main()
