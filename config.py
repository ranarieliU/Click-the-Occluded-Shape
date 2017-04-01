produce_heat_maps = True
run_avg_dist_analysis = True
run_radius_analysis = False

# If set to True, creates debug images `number_of_iterations` times.
# so for debugging - best to set `number_of_iterations` to 1
debug_images = True

images_subset = [1, 2, 3, 6, 7, 8, 11, 12, 13, 16, 17, 18]
run_subset = False

# Hexagon Binning Configuration
touches_threshold_list = [3]
grid_sizes_list = [70]

# # Analysis Configuration
number_iterations_list = [1]
sampled_points_list = [200]

# Threshold in pixels
radius_list = [20]


curr_clicks_threshold, curr_grid_size, curr_number_of_iterations, \
    curr_sampled_points, curr_radius_threshold = 0, 0, 0, 0, 0

remove_axes = False
show_plot = False

# folder names
paths_dic = {
    'orig_shapes': 'app_shapes',
    'csv_files': 'csv_files',
    'heat_maps': 'heat_maps',
    'prepared_for_medial_axis': 'shapes_prepared_for_medial_axis',
    'after_mfd': 'after_mfd',
    'medial_axised': 'clean_after_mfd',
    'debug': 'debug_images',
    'statistics': 'statistics'
}


colors_dic = {
    'red': (255, 0, 0),
    'white': (255, 255, 255),
    'blue': (0, 0, 255),
    'black': (0, 0, 0),
    'gray': (191, 191, 191)
}

shapes_dic = {}
for i in range(1, 9):
    shapes_dic[i] = 'new_%s.bmp' % str(i)
    shapes_dic[i+10] = 'new_%s_hidden.bmp' % str(i)

