############################################################################################################
# This step is taking the shapes resulting from step 3, producing heat maps and running analysis
#
# usage:
#
#   python run_step_4.py
#
############################################################################################################

import pylab as pl
import csv
from os import listdir
import os
import config
from os.path import isfile, join
import analysis
from PIL import Image
import random
import util
from util import join_path
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


def get_medial_axis(image):
    (width, height) = image.size
    medial_axis = []
    pix = image.load()
    for i in range(width):
        for j in range(height):
            rgb = pix[i, j]
            if list(rgb) == list(config.colors_dic['red']):
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
    image = pl.hexbin(x_list, y_list, C=None, gridsize=config.curr_grid_size,
                      bins=None, mincnt=config.curr_clicks_threshold, edgecolors='none')  # hexbinning
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
    return points[:config.curr_sampled_points]


def debugging_draw_points(size, image_name, touch_points, medial_axis, sampled_points, debug_path):
    util.create_new_path(debug_path)
    (width, height) = size
    new_img = Image.new('RGB', (width, height), "gray")
    draw_points(new_img, touch_points, config.colors_dic['blue'])
    draw_points(new_img, medial_axis, config.colors_dic['red'])
    draw_points(new_img, sampled_points, config.colors_dic['white'])
    new_img.save(join_path(debug_path, image_name))


def open_statistics_file(stat_path):
    util.create_new_path(stat_path)
    file_name = "statistics_%s_%s_%s_%s_%s" % (
        str(config.curr_grid_size), str(config.curr_clicks_threshold),
        str(config.curr_sampled_points), str(config.curr_number_of_iterations),
        str(config.curr_radius_threshold))
    stat_file = XlsxFile(join_path(stat_path, file_name))
    stat_file.create_file()
    headers = config.stat_headers
    stat_file.write_to_sheet(headers)
    return stat_file


def run(root_path):
    orig_shapes_path = join_path(root_path, paths_dic['orig_shapes'])
    csv_path = join_path(root_path, paths_dic['csv_files'])
    medial_axis_path = join_path(root_path, paths_dic['medial_axised'])
    heat_maps_path = join_path(root_path, paths_dic['heat_maps'])
    debug_path = join_path(root_path, paths_dic['debug'])
    statistics_path = join_path(root_path, paths_dic['statistics'])

    csv_files = [f for f in listdir(csv_path) if isfile(join(csv_path, f)) and f.endswith('.csv')]
    shapes_dic = config.shapes_dic
    stat_file = open_statistics_file(statistics_path)

    for csv_file in csv_files:
        x_list, y_list = read_csv(join_path(csv_path, csv_file))
        csv_suffix_location = csv_file.find('.csv')
        number = int(csv_file[0:csv_suffix_location])
        if config.run_subset:
            if number not in config.images_subset:
                continue
        image_name = shapes_dic[number]
        log.info('processing shape ' + image_name)
        img = util.read_image(join_path(medial_axis_path, util.get_image_name_clean_after_mfd(image_name)))

        # list of pairs (points) where touches have been made
        touch_points = list(zip(y_list, x_list))

        # list of pairs (points) of the medial axis
        medial_axis = get_medial_axis(img)

        orig_image = util.read_image(join_path(orig_shapes_path, image_name))
        unf_points = uniform_distribution(orig_image)

        image = plot_bins(img, x_list, y_list)
        hexbin_centers = bins_data(image)
        if config.produce_heat_maps:
            log.info("generating heat map")
            bmp_location = image_name.find('.bmp')
            new_image_name = image_name[0:bmp_location] + '_heat_map.png'
            util.create_new_path(heat_maps_path)
            pl.savefig(join_path(heat_maps_path, new_image_name), bbox_inches='tight', dpi=350)
        pl.close()

        pct_of_touches_in_radius, medial_axis_percentage, pct_of_medial_axis_and_radius, \
            avg_dist_touches_medial_axis, min_avg_dist_rand_points_medial_axis, avg_dist_ratio = [0, 0, 0, 0, 0, 0]

        if config.run_radius_analysis:
            log.info("running radius analysis")
            pct_of_medial_axis_and_radius = analysis.percent_in_range_2(unf_points, medial_axis)
            pct_of_touches_in_radius = analysis.percent_in_range_2(hexbin_centers, medial_axis)

        if config.run_avg_dist_analysis:
            log.info("running avg distance analysis")
            distances_sample = []
            for i in range(config.curr_number_of_iterations):
                sampled_points = take_sample(unf_points)
                distances_sample.append(
                    util.find_average_distance_from_medial_axis(sampled_points, medial_axis))
                if config.debug_images:
                    debugging_draw_points(img.size, image_name, touch_points, medial_axis, sampled_points, debug_path)

            medial_axis_percentage = float(len(medial_axis) / len(unf_points) * 100)
            avg_dist_touches_medial_axis = \
                util.find_average_distance_from_medial_axis(hexbin_centers, medial_axis)
            min_avg_dist_rand_points_medial_axis = min(distances_sample)
            avg_dist_ratio = min_avg_dist_rand_points_medial_axis / avg_dist_touches_medial_axis

        stat_row = [number, image_name, medial_axis_percentage,
                    pct_of_medial_axis_and_radius, pct_of_touches_in_radius,
                    avg_dist_touches_medial_axis, min_avg_dist_rand_points_medial_axis,
                    avg_dist_ratio, config.curr_grid_size, config.curr_clicks_threshold,
                    config.curr_sampled_points, config.curr_number_of_iterations, config.curr_radius_threshold]
        stat_file.write_to_sheet(stat_row)

    if config.produce_heat_maps:
        log.info("Saved heat maps to %s" % heat_maps_path)
    stat_file.save_workbook()
    log.info("Saved statistics file to %s" % statistics_path)
    if config.debug_images:
        log.info("Saved debugging images to %s" % debug_path)

    log.info('Finished successfully! Exiting...')
    os.chdir(root_path)


def main():

    log.info("Running step 4")

    root_path = os.getcwd()
    for grid_size in config.grid_sizes_list:
        for sampled_points in config.sampled_points_list:
            for iterations in config.number_iterations_list:
                for radius in config.radius_list:
                    for touch_threshold in config.touches_threshold_list:
                        [config.curr_clicks_threshold, config.curr_grid_size, config.curr_number_of_iterations,
                         config.curr_sampled_points, config.curr_radius_threshold] = \
                        [touch_threshold, grid_size, iterations, sampled_points, radius]
                        log.info("""
                        Running with configuration:
                        Clicks threshold: %d, Grid size: %d, Iterations: %d, Random sampled points: %d""" %
                                 (touch_threshold, grid_size, iterations, sampled_points))
                        run(root_path)


if __name__ == "__main__":
    main()
