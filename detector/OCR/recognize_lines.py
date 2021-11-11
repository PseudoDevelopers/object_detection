# Original code source: https://stackoverflow.com/questions/61347755/how-can-i-get-line-coordinates-that-readed-by-tesseract


import pytesseract
from pytesseract import Output

from config import *


def recognize_lines(img):
    texts = recognize_text(img)
    bbs = to_my_data_structure(texts)
    bbs = remove_low_confidence_texts(bbs)
    lines = words_to_lines(bbs)

    return lines


def recognize_text(img):
    texts = pytesseract.image_to_data(img, lang="eng", output_type=Output.DICT)
    return texts


def to_my_data_structure(texts):
    bounding_boxes = []

    n_boxes = len(texts['level'])
    for i in range(n_boxes):
        if texts['text'][i].strip() != '':
            bb = {
                'pos': (texts['left'][i], texts['top'][i]),
                'size': (texts['width'][i], texts['height'][i]),
                'val': texts['text'][i],
                'conf': texts['conf'][i],
                'block_num': texts['block_num'][i],
                'line_num': texts['line_num'][i],
            }
            bounding_boxes.append(bb)

    return bounding_boxes


def remove_low_confidence_texts(all_bbs):
    return [bb for bb in all_bbs if bb['conf'] > OCR_MIN_THRESHOLD]


def words_to_lines(bbs):
    # First we'll sort words in nested structure of blocks & lines
    data = {}

    for bb in bbs:
        block_num = bb['block_num']
        line_num = bb['line_num']

        if block_num in data:
            if line_num in data[block_num]:
                data[block_num][line_num].append(bb)
            else:
                data[block_num][line_num] = [bb]
        else:
            data[block_num] = {}
            data[block_num][line_num] = [bb]


    # Now we'll convert those blocks to lines
    lines = []
    for b in data.values():
        for l in b.values():
            sorted_line = sorted(l, key=lambda obj:obj['pos'][0])

            firstWord, lastWord = sorted_line[0], sorted_line[-1]
            width = lastWord['pos'][0]+lastWord['size'][0] - firstWord['pos'][0]
            height = max([h['size'][1] for h in sorted_line])

            val = ' '.join([t['val'] for t in sorted_line])

            line = {
                'size': (width, height),
                'pos': firstWord['pos'],
                'val': val
            }
            lines.append(line)

    return lines
