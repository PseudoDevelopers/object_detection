from math import atan, floor, degrees, sqrt


def process(objs):
    data = {}

    objs = find_areas(objs)
    objs = sort_wrt_area(objs)

    data['distanceRatio'] = find_distances_ratio(objs)
    data['angle'] = find_angles(objs)

    return data


def find_areas(objs):
    updatedObjs = [{**obj, 'area': obj['size'][0]*obj['size'][1]}
                   for obj in objs]

    return updatedObjs


def sort_wrt_area(objects):
    # Here we are sorting the objects
    # W.R.T Area. If area is equal then
    # W.R.T its pos corner
    sortedObjects = sorted(objects, reverse=True,
                           key=lambda obj: (obj['area'], -obj['pos'][1], -obj['pos'][0]))

    return sortedObjects


def find_distances_ratio(objects):
    obj1 = {}
    obj1['width'] = objects[0]['size'][0]
    obj1['height'] = objects[0]['size'][1]
    obj1['pos'] = objects[0]['pos']
    obj1['topRight'] = (obj1['pos'][0]+obj1['width'], obj1['pos'][1])
    obj1['bottomLeft'] = (obj1['pos'][0], obj1['pos'][1]+obj1['height'])
    obj1['bottomRight'] = (obj1['pos'][0]+obj1['width'],
                           obj1['pos'][1]+obj1['height'])

    obj2 = {}
    obj2['width'] = objects[1]['size'][0]
    obj2['height'] = objects[1]['size'][1]
    obj2['pos'] = objects[1]['pos']
    obj2['topRight'] = (obj2['pos'][0]+obj2['width'], obj2['pos'][1])
    obj2['bottomLeft'] = (obj2['pos'][0], obj2['pos'][1]+obj2['height'])
    obj2['bottomRight'] = (obj2['pos'][0]+obj2['width'],
                           obj2['pos'][1]+obj2['height'])

    posDistance = dist(obj1['pos'], obj2['pos'])
    bottomRightDistance = dist(obj1['bottomRight'], obj2['bottomRight'])
    firstDistanceRatio = posDistance / bottomRightDistance

    topRightDistance = dist(obj1['topRight'], obj2['topRight'])
    bottomLeftDistance = dist(obj1['bottomLeft'], obj2['bottomLeft'])
    secondDistanceRatio = topRightDistance / bottomLeftDistance

    finalDistanceRatio = firstDistanceRatio / secondDistanceRatio

    return floor(finalDistanceRatio)


def find_angles(objects):
    x = objects[0]['center'][0] - objects[1]['center'][0]
    y = objects[0]['center'][1] - objects[1]['center'][1]

    angle = degrees(atan(abs(y/x)))

    if x < 0 and y > 0:     # 2nd Quadrant
        angle = 180 - angle
    elif x < 0 and y < 0:   # 3rd Quandrant
        angle += 180
    elif x > 0 and y < 0:   # 4th Quandrant
        angle = 360 - angle

    return angle


def dist(p1, p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
