import pylab as pl
import csv
import time
from os import listdir
import os
import config
from os.path import isfile, join
import math
from PIL import Image
import random


def read_csv(file_name):
    x_list = []
    y_list = []
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x_list.append((float(row['X'])) / 2)
            y_list.append((float(row['Y'])) / 2)
    return x_list, y_list


def get_image(image_name):
    img = Image.open(image_name)
    rgb_im = img.convert('RGB')
    return rgb_im
    # return imread(image_name)


def get_image_2(image_name):
    im = Image.open(image_name)
    return im.convert('RGB')


def get_medial_axis(image):
    (width, height) = image.size
    medial_axis = []
    for i in range(width):
        for j in range(height):
            rgb = image.getpixel((i, j))
            if list(rgb) == [255, 0, 0]:
                medial_axis.append([j, i])
    return medial_axis


def draw_points(image, points, color):
    for point in points:
        x = point[0]
        y = point[1]
        image[x, y] = color
    return image


def plot_bins(img, x_list, y_list):
    pl.imshow(img, cmap=pl.get_cmap('Pastel1'))
    pl.plot()  # sub-plot area 2 out of 2
    image = pl.hexbin(x_list, y_list, C=None, gridsize=config.grid_size, bins=None, mincnt=config.clicks_threshold,
                      edgecolors='none')  # hexbinning
    # pl.scatter(X,Y,lw=0.5,c='k',edgecolor='w')  #overlaying the sample points
    pl.axis('image')  # necessary for correct aspect ratio
    fig = pl.imshow(img)
    # fig.axes.get_xaxis().set_visible(False)
    # fig.axes.get_yaxis().set_visible(False)
    # pl.axis('off')
    # pl.show()                                   #to show the plot
    return image


def bins_data(image):
    counts = image.get_array()
    # ncnts = np.count_nonzero(np.power(10,counts))
    verts = image.get_offsets()
    output = []
    for i, count in enumerate(counts):
        coord = [(verts[i][1], verts[i][0])]
        output += (coord * int(count))
    return output


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


def find_minimum_distance(src, target_list):
    return min(map(lambda x: math.sqrt((src[0] - x[0]) ** 2 + (src[1] - x[1]) ** 2), target_list))


def find_avarage_distance_from_medial_axis(points, medial_axis):
    # print(points[:5])
    minimum_dists = [find_minimum_distance(p, medial_axis) for p in points]
    # print(minimum_dists[:5])
    return sum(minimum_dists) / float(len(minimum_dists))


def uniform_distribution(image):
    (width, height) = image.size
    relevant_points = []
    for i in range(height):
        for j in range(width):
            r, g, b = image.getpixel((j, i))
            threshold = 245
            if all([x < threshold for x in [r, g, b]]):
                relevant_points.append([i, j])
    return relevant_points


def take_sample(points):
    n = 200
    random.shuffle(points)
    return points[:n]


def main():
    orig_path = os.getcwd()  # change if images are in another path (inner folder or something)
    csv_path = orig_path + '\\' + 'csv_files'
    csv_files = [f for f in listdir(csv_path) if isfile(join(csv_path, f)) and f.endswith('.csv')]
    shapes_dic = {1: 'triangle',
                  2: 'two_rectangles',
                  3: 'rectangle',
                  4: 'rectangle_missing',
                  5: 'rectangle_missing_2',
                  6: 'circle',
                  11: 'triangle_hidden',
                  12: 'two_rectangles_hidden',
                  13: 'rectangle_hidden',
                  14: 'rectangle_missing_hidden',
                  15: 'rectangle_missing_2_hidden',
                  16: 'circle_hidden',
                  17: 'a1_shape_hidden',
                  18: 'a2_shape_hidden',
                  19: 'a3_shape_hidden'}

    for k, v in shapes_dic.items():
        shapes_dic[k] += '.bmp'

    for csv_file in csv_files:
        orig_path = os.getcwd()
        os.chdir(csv_path)
        try:
            x_list, y_list = read_csv(csv_file)
        except UnicodeDecodeError:
            print('------------------')
            print(csv_file)
        os.chdir(orig_path)
        csv_suffix_location = csv_file.find('.csv')
        number = int(csv_file[0:csv_suffix_location])
        '''
        if number in [1, 2, 3, 4, 5, 6]:
            continue
        '''
        image_name = shapes_dic[number]
        medial_axised_path = os.getcwd() + '\\' + 'medial_axised_new_theorem'
        os.chdir(medial_axised_path)
        img = get_image(image_name)

        # list of pairs (points) where touches have been made
        touch_points = list(zip(y_list, x_list))

        # list of pairs (points) of the medial axis
        medial_axis = get_medial_axis(img)

        # print(find_avarage_distance_from_medial_axis(touch_points, medial_axis))

        os.chdir(orig_path)
        try:
            orig_image = get_image_2(image_name)
        except FileNotFoundError:
            print(os.getcwd())
        os.chdir(medial_axised_path)
        unf_points = uniform_distribution(orig_image)
        # print(find_avarage_distance_from_medial_axis(unf_points, medial_axis))

        print(image_name)
        image = plot_bins(img, x_list, y_list)
        hexbin_centres = bins_data(image)
        bmp_location = image_name.find('.bmp')
        new_image_name = image_name[0:bmp_location] + '.png'
        pl.savefig('heat_map_' + new_image_name, bbox_inches='tight', dpi=350)
        pl.close()
        os.chdir(orig_path)

        print('avg distance csv, medial axis', find_avarage_distance_from_medial_axis(hexbin_centres, medial_axis))
        distances_sample = []
        for i in range(config.number_of_iterations):
            sampled_points = take_sample(unf_points)
            distances_sample.append(find_avarage_distance_from_medial_axis(sampled_points, medial_axis))
            '''
            (height, width, dim) = img.shape
            bar = np.zeros([height, width, 3], dtype=np.uint8)
            bar.fill(0)
            red = (255, 0, 0)
            white = (255, 255, 255)
            blue = (0, 0, 255)
            bar = draw_points(bar, touch_points[:1], white)
            bar = draw_points(bar, medial_axis, red)
            # bar = draw_points(bar, sampled_points, white)
            bar_name = 'bar_' + image_name + '.png'
            imsave(bar_name, bar)
            '''
        print('avg distance uniform distribution, medial axis', min(distances_sample))


if __name__ == "__main__":
    main()
