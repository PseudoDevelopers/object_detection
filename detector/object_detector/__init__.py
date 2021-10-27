"""
This module actually detect & process the object from image.
"""


import cv2
import numpy as np

from config import OPEN_CV_MIN_THRESHOLD

from logger import log
_LOGGER = log(__name__)


def detect_objects(img):
    height, width, _ = img.shape
    
    detectedObjs = object_detector(img)
    processedObjs = process_objects(detectedObjs, width, height)
    removedDuplicatedObjs = remove_duplicated_objects(processedObjs)

    _LOGGER.info('Object detection is complete')
    return removedDuplicatedObjs


def object_detector(img):
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    height, width, channels = img.shape

    # Print all channels of images
    # for b in blob:
    #     for i, imgBlob in enumerate(b):
    #         cv2.imshow(str(i), imgBlob)

    net.setInput(blob)
    outs = net.forward(outputLayers)

    return outs


def process_objects(objs, width, height):
    processedObjs = []
    for obj in objs:
        for detection in obj:
            scores = detection[5:]
            classId = np.argmax(scores).item()
            confidence = scores[classId]

            if confidence > OPEN_CV_MIN_THRESHOLD:
                centerX = int(detection[0]*width)
                centerY = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)
                pos = (int(centerX-w/2), int(centerY-h/2))

                processedObjs.append({
                    'center': (centerX, centerY),
                    'size': (w, h),
                    'pos': pos,
                    'confidence': float(confidence),
                    'classId': classId
                })

    return processedObjs


def remove_duplicated_objects(objs):
    boxes = []
    classIds = []
    confidences = []
    for obj in objs:
        boxes.append([
            int(obj['center'][0]-obj['size'][0]/2),
            int(obj['center'][1]-obj['size'][1]/2),
            obj['size'][0],
            obj['size'][1]
        ])
        classIds.append(obj['classId'])
        confidences.append(obj['confidence'])

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    remainingObjects = [obj for i, obj in enumerate(objs) if i in indexes]

    return remainingObjects


net = cv2.dnn.readNet('detector/object_detector/yolov3-spp.weights',
                      'detector/object_detector/yolov3-spp.cfg')

layerNames = net.getLayerNames()
outputLayers = [layerNames[i[0]-1]for i in net.getUnconnectedOutLayers()]


if __name__ == '__main__':
    print(
"""This is a module to detect objects from an image.
Try importing & calling detect_objects(cv2.imread(<path_to_your_image>))
And it will return the detected objects from the image.
Good luck ;)"""
)
