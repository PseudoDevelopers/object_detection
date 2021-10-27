from math import floor


def process(obj):
    return {'widthHeightRatio': find_width_height_ratio(obj)}


def find_width_height_ratio(obj):
    return floor(obj['size'][0] / obj['size'][1])
