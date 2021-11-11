from .sub_imgs import find_sub_imgs
from .recognize_lines import recognize_lines

from ..show_img import mark_bounding_box

from config import GLOBAL_DEBUG
DEBUG_MODE = GLOBAL_DEBUG and False

from logger import log
_LOGGER = log(__name__)


def detect_text(img):
    subImgs = find_sub_imgs(img)
    _LOGGER.info(f'SubImgs: {len(subImgs)}')

    if DEBUG_MODE:
        # print(subImgs)
        mark_bounding_box(img, subImgs)

    lines = find_lines_in_sub_imgs(img, subImgs)
    lines = sort_lines(lines)

    _LOGGER.info('Text recognition is completed')
    return lines


def find_lines_in_sub_imgs(img, subImgs):
    lines = []

    for i in range(len(subImgs)):
        x, y = subImgs[i]['pos']
        w, h = subImgs[i]['size']

        # Cropping the text block for giving input to OCR
        cropped = img[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        newLines = recognize_lines(cropped)
        newLines = [{**line, 'pos': (line['pos'][0]+x, line['pos'][1]+y)} for line in newLines]
        lines += newLines

    return lines


def sort_lines(lines):
    return sorted(lines, key=lambda line: (line['pos'][1], line['pos'][0]))
