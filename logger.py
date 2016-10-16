import logging
log = logging.getLogger('Click_the_occluded_shape_logger')
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s')
ch.setFormatter(formatter)
log.addHandler(ch)