# The basics of machine learning and recognition

CZ: Semestrální práce k předmětu [KKY/ZSUR](http://www.kky.zcu.cz/cs/courses/zsur) na katedře kybernetiky Západočeské univerzity v Plzni.

[//]: # (Teacher Ing. Mgr. Josef V. Psutka, Ph.D. - 2017/2018)

EN: Term paper for subject "The basics of machine learning and recognition" at University of West Bohemia in Pilsen.

## Running project

Run project in console by typing in project folder `$ python -m zsur`, or by running `__main__.py` file directly. But it will run the *main* file only. It is going to plot specified set of points.

To get machine learning methods from project, you have to run relevant .py file.

### How many classes is in data?

1. cluster_levels.py
2. chain_map.py
3. maximin.py

### Divide data into classes

1. kmeans.py
2. unequal_binary.py

### Classifiers

1. bayes.py
2. minimal_distance.py
3. nearest_neighbour.py
4. linear_disc.py

## Technical information

```sh
$ python
Python 3.6.4 | Anaconda (64-bit)
```

Read requirements.txt!

!Warning! Data from **k-means** algorithm are in Python dictionary like this one: {(center_of_cluster): [(point), (point), ...], ...} 

## Additional information

Project structure and setup taken from [chriswarrick.com][1].

[1]: https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
