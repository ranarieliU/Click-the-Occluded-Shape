import config
import util


def percent_in_range(points, medial_axis):
    count_touches = len(points)
    distances = map(lambda x: util.find_minimum_distance(x, medial_axis), points)
    filtered_distances = list(filter(lambda x: x <= config.radius_threshold, distances))
    return float(len(filtered_distances) / count_touches * 100)
