############################################################################################################
# This step is taking the shapes resulting from step 1 and running the mfd
#
# ### Only works on Windows / Linus ###
#
# usage:
#
#   python3 run_step_2.py
#
############################################################################################################

import os
from os import listdir
from os.path import isfile, join
import config
import util
from logger import log


def run(before_mfd_folder, shape_name, output_folder):
    command = "mfd -m %s -md → %s" % (util.join_path(before_mfd_folder, shape_name), output_folder)
    os.system(command)


def main():

    log.info("Running step 2")

    mfd_folder = util.join_path(os.getcwd(), config.paths_dic['mfd'])
    before_mfd_folder = util.join_path(os.getcwd(), config.paths_dic['prepared_for_mfd'])
    output_folder = util.join_path(os.getcwd(), config.paths_dic['after_mfd'])

    os.chdir(mfd_folder)

    shapes_names = [f for f in listdir(before_mfd_folder) if isfile(join(before_mfd_folder, f)) and f.endswith('.bmp')]

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for shape_name in shapes_names:
        run(before_mfd_folder, shape_name, output_folder)

    log.info("Images after mfd saved to %s" % output_folder)
    log.info("----------------- Finished Successfully -----------------")


if __name__ == "__main__":
    main()