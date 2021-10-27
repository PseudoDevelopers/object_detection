from os import rename as move_file, remove as del_file
import json

from flask import Flask, render_template, redirect

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


# When user only submits
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


# When user search
# @app.route('/search', methods=['POST'])
# @validate_submit_search_form
# def search_img(img_name):
#     objs, objs_for_search = detect_objs(img_name, add_deviation=True)

#     if objs is None:
#         # TODO: The image should be deleted
#         return send_respose('no_img_found')

#     imgs = search_objs_in_db(objs_for_search)
#     move_file(UPLOADED_IMGS_DIR+img_name, INDEXED_IMGS_DIR+img_name)
#     insert_graphical_img_data(objs)

#     if imgs is None:
#         return send_respose('no_img_found')

#     imgs = [INDEXED_IMGS_DIR+img for img in imgs]
#     return send_respose('gallary', imgs=imgs)


# When user request to verify document
# @app.route('/search-document', methods=['POST'])
# @validate_submit_search_form
# def search_document(img_name):
#     objs, bbs = document_detertor(img_name)

#     if objs is None or bbs is None:
#         # TODO: Case for 0 or 1 objs
#         # TODO: The image should be deleted
#         return send_respose('no_img_found')

#     indexed = index_bounding_boxes(objs, True, len(bbs), add_deviation=True)
#     imgs = search_documents_in_db(indexed)

#     if imgs is None:
#         return send_respose('no_img_found')

#     imgs = [INDEXED_IMGS_DIR+img for img in imgs]
#     return send_respose('gallary', imgs=imgs)


# When user submit document template
# Then server send the bounding boxes to client to select types of bounding boxes
# This route used only when user submits types of bounding boxes
@app.route('/document-bounding-boxes-selector', methods=['POST'])
@validate_bounding_boxes_selector_form
def save_template(imgName, graphicalObjs, BBs):
    _LOGGER.info('BBs recieved')
    indexed = process_and_index(graphicalObjs, BBs, imgName)
    insert_to_db(indexed)
    _LOGGER.info('Data inserted to DB')

    return redirect('/')


def send_respose(template, *args, **kwargs):
    return render_template('index.html', template=template, *args, **kwargs)


if __name__ == '__main__':
    print(f'\n{" "*10}*'*5)
    app.run(debug=True)
