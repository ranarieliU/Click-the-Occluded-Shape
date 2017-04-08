############################################################################################################
# This step is taking the shapes resulting from step 2,
#   removing the noise (extra red lines) and returning frame to white
#
# usage:
#
#   python run_step_3.py
#
############################################################################################################

from os import listdir
from util import join_path
import config
from config import paths_dic
import os
import util
from logger import log
from os.path import isfile, join


def clean_outside_red_lines(orig_shape, shape_after_mfd):
    pixels_orig = orig_shape.load()
    pixels_after = shape_after_mfd.load()
    width, height = orig_shape.size
    for i in range(height):
        for j in range(width):
            orig_color = pixels_orig[j, i]
            after_mfd_color = pixels_after[j, i]
            if orig_color == config.colors_dic['white'] and after_mfd_color != config.colors_dic['black']:
                pixels_after[j, i] = config.colors_dic['black']
    return shape_after_mfd


def override_frame(shape_before_mfd, shape_after_mfd):
    pixels_before = shape_before_mfd.load()
    pixels_after = shape_after_mfd.load()
    width, height = shape_before_mfd.size
    for i in range(height):
        for j in range(width):
            curr_color = pixels_before[j, i]
            if curr_color == config.colors_dic['white']:
                pixels_after[j, i] = config.colors_dic['white']
    return shape_after_mfd


def run(orig_shape_name, orig_folder, before_mfd_folder, after_mfd_folder, output_folder):

    log.info("Processing %s" % orig_shape_name)

    orig_shape_path = join_path(orig_folder, orig_shape_name)
    before_mfd_path = join_path(before_mfd_folder, util.get_binary_image_name(orig_shape_name))
    after_mfd_image_name = util.get_image_name_clean_after_mfd(orig_shape_name)
    after_mfd_path = join_path(after_mfd_folder, after_mfd_image_name)
    output_image_name = after_mfd_image_name

    orig_shape = util.read_image(orig_shape_path)
    shape_before_mfd = util.read_image(before_mfd_path)
    shape_after_mfd = util.read_image(after_mfd_path)

    log.info("Overriding shape frame: red -> white")
    clean_img = override_frame(shape_before_mfd, shape_after_mfd)

    log.info("Overriding outside shape red lines: red -> black")
    clean_img = clean_outside_red_lines(orig_shape, clean_img)

    log.info("Saving clean image")
    util.save_on_path(clean_img, output_image_name, output_folder)


def main():

    log.info("Running step 3")

    orig_folder = join_path(os.getcwd(), paths_dic['orig_shapes'])
    orig_shapes_names = [f for f in listdir(orig_folder) if isfile(join(orig_folder, f)) and f.endswith('.bmp')]

    before_mfd_folder = join_path(os.getcwd(), paths_dic['prepared_for_mfd'])
    after_mfd_folder = join_path(os.getcwd(), paths_dic['after_mfd'])
    output_folder = join_path(os.getcwd(), paths_dic['medial_axised'])

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for orig_shape_name in orig_shapes_names:
        run(orig_shape_name, orig_folder, before_mfd_folder, after_mfd_folder, output_folder)

    log.info("----------------- Finished Successfully -----------------")


if __name__ == "__main__":
    main()
