# hexbins configurations
clicks_threshold = 3
grid_size = 70

'''
touches_threshold_list = [3, 4]
grid_sizes_list = [70, 50]
number_iterations_list = [1000]
sampled_points_list = [1000]
radius_list = [15, 20, 25]
'''

# which parts to run - configurations

# use new medial axis theorem
new_medial_axis = False

curve_completion = False

# create heat maps
create_heat_maps = True

# if set to True, creates debug images `number_of_iterations` times.
# so for debugging - best to set `number_of_iterations` to 1
debug_images = False

do_all_analysis = False
do_radius_analysis = False

# not_hidden_images_numbers = [1, 2, 3, 4, 5, 6]
not_hidden_images_numbers = [1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 17, 18, 19]
process_only_hidden_images = True


touches_threshold_list = [3]
grid_sizes_list = [70]
number_iterations_list = [1]
sampled_points_list = [200]
radius_list = [1]


number_of_iterations = 1

sampled_points = 200

remove_axes = False
show_plot = False

# directories names dic
paths_dic = {
    'orig_shapes': 'orig_shapes',
    'csv_files': 'csv_files',
    'heat_maps': 'heat_maps',
    'medial_axis': 'medial_axised',
    'medial_axis_new_theorem': 'medial_axised_new_theorem',
    'debug': 'debug_images',
    'statistics': 'statistics',
    'curve_completion': 'curve_completion'
}


# pixels threshold
radius_threshold = 20

# colors
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)

shapes_dic = {1: 'triangle.bmp',
              2: 'two_rectangles.bmp',
              3: 'rectangle.bmp',
              4: 'rectangle_missing.bmp',
              5: 'rectangle_missing_2.bmp',
              6: 'circle.bmp',
              11: 'triangle_hidden.bmp',
              12: 'two_rectangles_hidden.bmp',
              13: 'rectangle_hidden.bmp',
              14: 'rectangle_missing_hidden.bmp',
              15: 'rectangle_missing_2_hidden.bmp',
              16: 'circle_hidden.bmp',
              17: 'a1_shape_hidden.bmp',
              18: 'a2_shape_hidden.bmp',
              19: 'a3_shape_hidden.bmp'}

