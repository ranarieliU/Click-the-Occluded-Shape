from os import listdir
from util import join_path
import config
from config import paths_dic
import os
import util
from logger import log
from os.path import isfile, join


# utility func for calc_boundaries
def is_boundary(image, coord):
    width, height = image.size
    x, y = coord
    r, g, b = image.getpixel((x, y))
    # If current pixel is white -> not a boundary
    if r > 245 and g > 245 and b > 245:
        return False
    if x == 0 or y == 0 or x == width - 1 or y == height - 1:
        return True
    # If current pixel is gray and has neighbor that is not gray -> a boundary
    for i in [-1, 1]:
        coord_1 = image.getpixel((x + i, y))  # Left, Right
        coord_2 = image.getpixel((x, y + i))  # Down, Up
        if coord_1 != config.colors_dic['gray'] or coord_2 != config.colors_dic['gray']:
            return True
    return False


# will get an image that has been read as param, will return a list of (X,Y) coordinates that are the image boundaries
def calc_boundaries(image):
    ans = []
    width, height = image.size
    for i in range(height):
        for j in range(width):
            if is_boundary(image, (j, i)):
                ans.append((j, i))
    return ans


def improve_coloring(image):
    width, height = image.size
    pixels = image.load()
    for i in range(height):
        for j in range(width):
            r, g, b = image.getpixel((j, i))
            if r < 235 or g < 235 or b < 235:
                pixels[j, i] = config.colors_dic['gray']
            else:
                pixels[j, i] = config.colors_dic['white']
    return image


def whiten(image):
    pixels = image.load()
    width, height = image.size
    for i in range(height):
        for j in range(width):
            curr_color = pixels[j, i]
            if 0 < curr_color[0] < 255:
                pixels[j, i] = config.colors_dic['white']
    return image


def replace_white_and_black(image):
    pixels = image.load()
    width, height = image.size
    for i in range(height):
        for j in range(width):
            curr_color = pixels[j, i]
            if curr_color[0] == 0:
                pixels[j, i] = config.colors_dic['white']
            elif curr_color[0] == 255:
                pixels[j, i] = config.colors_dic['black']
    return image


def mark_boundary(image, boundaries, color):
    pixels = image.load()
    for x, y in boundaries:
        pixels[x, y] = color
    return image


def run_funcs(orig_shape_name, folder_input_path, folder_output_path):
    shape_input_path = join_path(folder_input_path, orig_shape_name)
    output_image_name = 'binary_%s' % orig_shape_name

    log.info("Reading %s" % orig_shape_name)
    image = util.read_image(shape_input_path)

    log.info("Improving shape coloring")
    image = improve_coloring(image)

    log.info("Calculating boundaries")
    boundaries = calc_boundaries(image)

    log.info("Marking boundary")
    image = mark_boundary(image, boundaries, config.colors_dic['black'])

    log.info("Building binary")
    image = whiten(image)
    image = replace_white_and_black(image)

    util.save_on_path(image, output_image_name, folder_output_path)
    log.info("New shape %s saved on %s" % (output_image_name, folder_output_path))


def main():
    input_folder = join_path(os.getcwd(), paths_dic['orig_shapes'])
    orig_shapes_names = [f for f in listdir(input_folder) if isfile(join(input_folder, f)) and f.endswith('.bmp')]

    output_folder = join_path(os.getcwd(), paths_dic['prepared_for_mfd'])
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for orig_shape_name in orig_shapes_names:
        run_funcs(orig_shape_name, input_folder, output_folder)

    log.info("Images prepared for mfd saved to %s" % output_folder)
    log.info("----------------- Finished Successfully -----------------")


if __name__ == "__main__":
    main()
