# Original code source: https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/


import cv2

from config import GLOBAL_DEBUG


DEBUG_MODE = GLOBAL_DEBUG and True


def find_sub_imgs(img):
    thresh = preprocessing(img)
    contours = find_contours(thresh)
    subImgs = contours_to_sub_imgs_coordinates(img, contours)

    return subImgs


def preprocessing(img):
    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert image to binary image
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    return thresh


def find_contours(thresh):
    # Performing OTSU threshold
    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Appplying dilation on the threshold image
    dilation = cv2.dilate(thresh, rect_kernel, iterations=1)

    # Finding contours
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours


def contours_to_sub_imgs_coordinates(img, contours):
    subImgs = []
    imgSize = img.shape[0:2]

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if (h, w) != imgSize:
            # Some times OpenCV add whole image as one contour
            # So we have to ignore this
            subImgs.append({
                'pos': (x, y),
                'size': (w, h)
            })

    return subImgs
