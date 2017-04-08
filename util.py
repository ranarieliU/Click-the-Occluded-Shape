from os import listdir
from os.path import isfile, join
from PIL import Image
from os import getcwd
import pylab as pl
import time
import os.path
import math
from collections import namedtuple


def read_image(path):
    im = Image.open(path)
    rgb_im = im.convert('RGB')
    return rgb_im


def get_binary_image_name(orig_name):
    return 'binary_%s' % orig_name


def get_image_name_clean_after_mfd(orig_name):
    orig_without_suffix = orig_name[:orig_name.find('.bmp')]
    # orig_without_suffix = orig_name.split('.')[0]
    return 'binary_%s_med.bmp' % orig_without_suffix


def find_minimum_distance(src, target_list):
    return min(map(lambda x: math.sqrt((src[0] - x[0]) ** 2 + (src[1] - x[1]) ** 2), target_list))


def find_average_distance_from_medial_axis(points, medial_axis):
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


def get_diff_colors(image, print_dic=False):
    (width, height) = image.size
    Color = namedtuple("Color", ["r", "g", "b"])
    diff_colors = {}
    pix = image.load()
    for i in range(height):
        for j in range(width):
            rgb = list(pix[j, i])
            c = Color(*rgb)
            if c not in diff_colors:
                diff_colors[c] = 1
            else:
                diff_colors[c] += 1
    if print_dic:
        total_pixels = sum(diff_colors.values())
        for k, v in diff_colors.items():
            print("{} cnt: {:d} ({:.2f}%)".format(k, v, v / float(total_pixels) * 100))
    return diff_colors
