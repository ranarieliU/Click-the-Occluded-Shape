import pylab as pl
import csv
from os import listdir
import os
import config
from os.path import isfile, join
import analysis
from PIL import Image
import random
import general_functions
from config import paths_dic
from xlsx_files import XlsxFile
from logger import log


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


def get_medial_axis(image):
    (width, height) = image.size
    medial_axis = []
    pix = image.load()
    for i in range(width):
        for j in range(height):
            rgb = pix[i, j]
            if list(rgb) == list(config.red):
                medial_axis.append([j, i])
    return medial_axis


def draw_points(image, points, color):
    pix = image.load()
    for point in points:
        x = point[0]
        y = point[1]
        pix[y, x] = color


def plot_bins(img, x_list, y_list):
    pl.imshow(img, cmap=pl.get_cmap('Pastel1'))
    pl.plot()  # sub-plot area 2 out of 2
    image = pl.hexbin(x_list, y_list, C=None, gridsize=config.grid_size,
                      bins=None, mincnt=config.clicks_threshold, edgecolors='none')  # hexbinning
    # pl.scatter(X,Y,lw=0.5,c='k',edgecolor='w')  # overlaying the sample points
    pl.axis('image')  # necessary for correct aspect ratio
    fig = pl.imshow(img)
    if config.remove_axes:
        fig.axes.get_xaxis().set_visible(False)
        fig.axes.get_yaxis().set_visible(False)
        pl.axis('off')
    if config.show_plot:
        pl.show()
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


def uniform_distribution(image):
    (width, height) = image.size
    relevant_points = []
    pix = image.load()
    for i in range(height):
        for j in range(width):
            rgb = list(pix[j, i])
            threshold = 245
            if all([x < threshold for x in rgb]):
                relevant_points.append([i, j])
    return relevant_points


def take_sample(points):
    random.shuffle(points)
    return points[:config.sampled_points]


def debugging_draw_points(size, image_name, touch_points, medial_axis, sampled_points, debug_path):
    general_functions.create_new_path(debug_path)
    (width, height) = size
    new_img = Image.new('RGB', (width, height), "gray")
    # draw_points(new_img, touch_points, config.white)
    draw_points(new_img, medial_axis, config.red)
    draw_points(new_img, sampled_points, config.white)
    new_img.save(concatenate_dirs(debug_path, image_name))


def concatenate_dirs(dir1, dir2):
    return dir1 + '/' + dir2


def open_statistics_file(stat_path):
    general_functions.create_new_path(stat_path)
    file_name = 'statistics_' + str(config.grid_size) + '_' + str(config.clicks_threshold) + \
                '_' + str(config.sampled_points) + '_' + str(config.number_of_iterations)
    stat_file = XlsxFile(concatenate_dirs(stat_path, file_name))
    stat_file.create_file()
    headers = ['number', 'image_name', '% medial axis', '% medial axis and radius', '% touches in radius',
               'avg dist touches <-> medial_axis',
               'avg dist rand_points <-> medial_axis', 'ratio', 'grid_size', 'clicks_threshold',
               'sampled_points', 'iterations', 'radius']
    stat_file.write_to_sheet(headers)
    return stat_file


def run(root_path):
    orig_shapes_path = concatenate_dirs(root_path, paths_dic['orig_shapes'])
    csv_path = concatenate_dirs(root_path, paths_dic['csv_files'])
    medial_axis_old_path = concatenate_dirs(root_path, paths_dic['medial_axis'])
    medial_axis_new_path = concatenate_dirs(root_path, paths_dic['medial_axis_new_theorem'])
    curve_completion_path = concatenate_dirs(root_path, paths_dic['curve_completion'])
    heat_maps_path = concatenate_dirs(root_path, paths_dic['heat_maps'])
    debug_path = concatenate_dirs(root_path, paths_dic['debug'])
    statistics_path = concatenate_dirs(root_path, paths_dic['statistics'])

    csv_files = [f for f in listdir(csv_path) if isfile(join(csv_path, f)) and f.endswith('.csv')]
    shapes_dic = config.shapes_dic
    stat_file = open_statistics_file(statistics_path)

    for csv_file in csv_files:
        x_list, y_list = read_csv(concatenate_dirs(csv_path, csv_file))
        csv_suffix_location = csv_file.find('.csv')
        number = int(csv_file[0:csv_suffix_location])
        if config.process_only_hidden_images:
            if number in config.not_hidden_images_numbers:
                continue
        image_name = shapes_dic[number]
        shape_name = image_name[:image_name.find('.bmp')]
        log.info('processing shape ' + shape_name)
        if config.new_medial_axis:
            img = get_image(concatenate_dirs(medial_axis_new_path, image_name))
        elif config.curve_completion:
            img = get_image(concatenate_dirs(curve_completion_path, image_name))
        else:
            img = get_image(concatenate_dirs(medial_axis_old_path, image_name))

        # list of pairs (points) where touches have been made
        touch_points = list(zip(y_list, x_list))

        # list of pairs (points) of the medial axis
        medial_axis = get_medial_axis(img)

        orig_image = get_image(concatenate_dirs(orig_shapes_path, image_name))
        unf_points = uniform_distribution(orig_image)

        image = plot_bins(img, x_list, y_list)
        hexbin_centres = bins_data(image)
        if config.create_heat_maps:
            bmp_location = image_name.find('.bmp')
            new_image_name = image_name[0:bmp_location] + '_heat_map.png'
            general_functions.create_new_path(heat_maps_path)
            pl.savefig(concatenate_dirs(heat_maps_path, new_image_name), bbox_inches='tight', dpi=350)
        pl.close()

        distances_sample = []
        for i in range(config.number_of_iterations):
            sampled_points = take_sample(unf_points)
            distances_sample.append(
                general_functions.find_avarage_distance_from_medial_axis(sampled_points, medial_axis))
            if config.debug_images:
                debugging_draw_points(img.size, image_name, touch_points, medial_axis, sampled_points, debug_path)

        # statistics
        medial_axis_percentage = float(len(medial_axis) / len(unf_points) * 100)
        if config.do_all_analysis:
            if config.do_radius_analysis:
                percentage_in_radius = analysis.percent_in_range(hexbin_centres, medial_axis)
                percentage_of_medial_axis_and_radius = analysis.percent_in_range(unf_points, medial_axis)
            else:
                percentage_in_radius = 0
                percentage_of_medial_axis_and_radius = 0
            avg_dist_touches_medial_axis = \
                general_functions.find_avarage_distance_from_medial_axis(hexbin_centres, medial_axis)
            min_avg_dist_rand_points_medial_axis = min(distances_sample)
            avg_dist_ratio = min_avg_dist_rand_points_medial_axis / avg_dist_touches_medial_axis
        else:
            percentage_in_radius, percentage_of_medial_axis_and_radius, avg_dist_touches_medial_axis, \
                min_avg_dist_rand_points_medial_axis, avg_dist_ratio = [0, 0, 0, 0, 0]

        stat_row = [number, shape_name, medial_axis_percentage, percentage_in_radius,
                    percentage_of_medial_axis_and_radius,
                    avg_dist_touches_medial_axis, min_avg_dist_rand_points_medial_axis,
                    avg_dist_ratio, config.grid_size, config.clicks_threshold,
                    config.sampled_points, config.number_of_iterations, config.radius_threshold]
        stat_file.write_to_sheet(stat_row)

    log.info('Finished successfully! Exiting...')

    stat_file.save_workbook()
    os.chdir(root_path)


def main():
    root_path = os.getcwd()
    for grid_size in config.grid_sizes_list:
        for sampled_points in config.sampled_points_list:
            for iterations in config.number_iterations_list:
                for radius in config.radius_list:
                    for touch_threshold in config.touches_threshold_list:
                        [config.clicks_threshold, config.grid_size, config.number_of_iterations,
                         config.sampled_points, config.radius_threshold] = \
                        [touch_threshold, grid_size, iterations, sampled_points, radius]
                        log.info(str(touch_threshold) + ' ' + str(grid_size) + ' ' +
                                 str(iterations) + ' ' + str(sampled_points) + ' ' + str(radius))
                        run(root_path)


if __name__ == "__main__":
    main()
