from os import listdir
from os.path import isfile, join
from os import getcwd
# from PIL import Image
import pylab as pl
import time
import os.path
import math


def find_minimum_distance(src, target_list):
    return min(map(lambda x: math.sqrt((src[0] - x[0]) ** 2 + (src[1] - x[1]) ** 2), target_list))


def find_avarage_distance_from_medial_axis(points, medial_axis):
    minimum_dists = [find_minimum_distance(p, medial_axis) for p in points]
    return sum(minimum_dists) / float(len(minimum_dists))


# debugging function - prints files in current directory
def print_files_in_dir():
    curr_path = getcwd()
    onlyfiles = [f for f in listdir(curr_path) if isfile(join(curr_path, f))]
    print(onlyfiles)


def join_path(dir1, dir2):
    import os
    return os.path.join(dir1, dir2)


def create_new_path(new_path):
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    os.chdir(new_path)


def save_on_path(image, image_name, save_path):
    cur = os.getcwd()
    os.chdir(save_path)
    image.save(image_name)
    os.chdir(cur)


def show_all_colors(img):
    list = ['Pastel1', 'terrain', 'PuRd_r', 'Greys', 'Blues', 'BuGn', 'BuPu',
            'GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd',
            'PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu',
            'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd',
            'afmhot', 'autumn', 'bone', 'cool',
            'copper', 'gist_heat', 'gray', 'hot',
            'pink', 'spring', 'summer', 'winter',
            'BrBG', 'bwr', 'coolwarm', 'PiYG', 'PRGn', 'PuOr',
            'RdBu', 'RdGy', 'RdYlBu', 'RdYlGn', 'Spectral',
            'seismic', 'Accent', 'Dark2', 'Paired',
            'Pastel2', 'Set1', 'Set2', 'Set3',
            'gist_earth', 'ocean', 'gist_stern',
            'brg', 'CMRmap', 'cubehelix',
            'gnuplot', 'gnuplot2', 'gist_ncar',
            'nipy_spectral', 'jet', 'rainbow',
            'gist_rainbow', 'hsv', 'flag', 'prism']
    for color in list:
        print(color)
        pl.imshow(img, cmap=pl.get_cmap(color))
        pl.show()
        time.sleep(2)
        pl.close()
