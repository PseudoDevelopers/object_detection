"""
This module show image along with there objects & text bounding boxes.
This is used just in debugging.
"""


import cv2
import numpy as np


# This function marks detected obecjs & texts
# And show in a window
def show_img(img, objects=None, texts=None):
    if objects is not None:
        mark_objects(img, objects)
    if texts is not None:
        mark_bounding_box(img, texts)

    scaleFactor = calc_scale_factor(img.shape)

    img = cv2.resize(img, None, fx=scaleFactor, fy=scaleFactor)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Marks the given objects
def mark_objects(img, objects):
    for i, obj in enumerate(objects):
        label = classes[obj['classId']]

        bottomRight = (obj['pos'][0]+obj['size'][0],
                       obj['pos'][1]+obj['size'][1])
        pos = obj['pos']
        cv2.rectangle(img, pos, bottomRight, colors[i], 2, 500)
        cv2.putText(img, label, pos,
                    cv2.FONT_HERSHEY_PLAIN, 3, colors[i], 3)


def show_bounding_boxes(img, BBs):
    mark_bounding_box(img, BBs)
    
    scaleFactor = calc_scale_factor(img.shape)

    img = cv2.resize(img, None, fx=scaleFactor, fy=scaleFactor)
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Marks the given texts
def mark_bounding_box(img, BBs):
    for text in BBs:
        bottomRight = (text['pos'][0]+text['size']
                       [0], text['pos'][1]+text['size'][1])
        cv2.rectangle(img, text['pos'], bottomRight, (0, 255, 0), 2)


def calc_scale_factor(shape):
    scaleFactor = min(
        1000 / shape[0],
        1000 / shape[1]
    )
    return scaleFactor


# Reading the class names
classes = []
with open('detector/show_img/coco.names', 'r') as f:
    classes = [line.strip() for line in f.readlines()]
# Defining different colors for each class
colors = np.random.uniform(0, 255, size=(len(classes), 3))
