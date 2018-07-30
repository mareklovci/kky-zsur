from pathlib import Path


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
    my_file = Path(infile)  # run with command line
    if not my_file.is_file():
        my_file = Path('../' + infile)  # run directly __main__.py
    return rf(my_file)


def main():
    pass


if __name__ == '__main__':
    main()
