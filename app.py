from os import rename as move_file, remove as del_file
import json

from flask import Flask, render_template, redirect, send_from_directory

# Local imports
from config import *
from logger import log
from detector import detect_objs_and_text
from indexing import process_and_index, process_and_index_for_submit_search
from DB import insert_to_db
from DB.search import search_from_db
from validation import validate_submit_search_form, validate_bounding_boxes_selector_form


app = Flask(__name__)
_LOGGER = log(__name__)


# Index page
@app.route('/')
def index():
    return send_respose('default')


# Submitting an image
@app.route('/submit', methods=['POST'])
@validate_submit_search_form
def submit_img(imgName):
    graphicalObjs, textualObjs = detect_objs_and_text(imgName)

    if len(graphicalObjs) == 0 and len(textualObjs) == 0:
        del_file(f'{UPLOADED_IMGS_DIR}/{imgName}')
        return redirect('/')

    elif len(textualObjs) == 0:
        move_file(UPLOADED_IMGS_DIR+imgName, INDEXED_IMGS_DIR+imgName)
        indexed = process_and_index(graphicalObjs, {'SBBs': [], 'DBBs': [], 'DBBs': []}, imgName)
        insert_to_db(indexed)
        return redirect('/')

    return send_respose(
        template='document-bounding-boxes-selector',
        img={ 'name': imgName, 'path': UPLOADED_IMGS_DIR },
        bounding_boxes=json.dumps(textualObjs),
        objs=json.dumps(graphicalObjs)
    )


# Searching an image
@app.route('/search', methods=['POST'])
@validate_submit_search_form
def search_img(imgName):
    graphicalObjs, textualObjs = detect_objs_and_text(imgName)

    if len(graphicalObjs) == 0 and len(textualObjs) == 0:
        del_file(f'{UPLOADED_IMGS_DIR}/{imgName}')
        return send_respose('no_img_found')

    move_file(UPLOADED_IMGS_DIR+imgName, INDEXED_IMGS_DIR+imgName)

    BBs = {'SBBs': textualObjs, 'DBBs': [], 'UBBs': []}
    indexedForSubmit, dataForSearch = process_and_index_for_submit_search(
        graphicalObjs, BBs, imgName)

    imgs = search_from_db(dataForSearch)

    insert_to_db(indexedForSubmit)
    _LOGGER.info('Image searching completed\n')

    if len(imgs) == 0:
        return send_respose('no_img_found')

    # imgs = [INDEXED_IMGS_DIR+img for img in imgs]
    return send_respose('gallary', imgs=imgs)


# When user submit document template
# Then server send the bounding boxes to client to select types of bounding boxes
# This route used only when user submits types of bounding boxes
@app.route('/bbs-submit', methods=['POST'])
@validate_bounding_boxes_selector_form
def save_template(imgName, graphicalObjs, BBs):
    move_file(UPLOADED_IMGS_DIR+imgName, INDEXED_IMGS_DIR+imgName)
    
    _LOGGER.info('BBs recieved')
    indexed = process_and_index(graphicalObjs, BBs, imgName)
    insert_to_db(indexed)
    _LOGGER.info('Data inserted to DB')

    return redirect('/')


def send_respose(template, *args, **kwargs):
    return render_template('index.html', template=template, *args, **kwargs)


@app.route('/uploaded/<path:filename>')
def get_uploaded_img(filename):
    return send_from_directory(UPLOADED_IMGS_DIR, filename, as_attachment=True)


@app.route('/indexed/<path:filename>')
def get_indexed_img(filename):
    return send_from_directory(INDEXED_IMGS_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    print(f'\n{" "*10}*'*5)
    app.run(debug=True)
