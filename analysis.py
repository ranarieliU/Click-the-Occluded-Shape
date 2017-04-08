import config
import util
from math import sqrt


def percent_in_range(points, medial_axis):
    # Complexity:
    # n = len(points)
    # m = len(medial_axis)
    # Complexity O(n*m)
    count_touches = len(points)
    distances = map(lambda x: util.find_minimum_distance(x, medial_axis), points)
    filtered_distances = list(filter(lambda x: x <= config.curr_radius_threshold, distances))
    return float(len(filtered_distances) / count_touches * 100)


def percent_in_range_2(points, medial_axis):
    # Complexity:
    # n = len(points)
    # m = len(medial_axis)
    # Avg case: O(n + m)
    s = set()
    for element in medial_axis:
        s.add((int(element[0]), int(element[1])))
    medial_axis = s
    total_cnt = len(points)
    in_range_cnt = 0
    for p in points:
        p = (int(p[0]), int(p[1]))
        point_in_range = False
        for i in range(config.curr_radius_threshold + 1):
            if point_in_range:
                break
            coords = [(p[0] + i, p[1]), (p[0] - i, p[1]), (p[0], p[1] + i), (p[0], p[1] - i)]
            for coord in coords:
                if coord in medial_axis:
                    in_range_cnt += 1
                    point_in_range = True
                    break
        if point_in_range:
            continue
        diagonal_range = int(config.curr_radius_threshold / sqrt(2))
        for i in range(diagonal_range + 1):
            if point_in_range:
                break
            coords = [(p[0] + i, p[1] + i), (p[0] - i, p[1] - i), (p[0] - i, p[1] + i), (p[0] + i, p[1] - i)]
            for coord in coords:
                if coord in medial_axis:
                    in_range_cnt += 1
                    point_in_range = True
                    break
    return in_range_cnt / float(total_cnt) * 100