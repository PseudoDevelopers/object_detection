from os.path import splitext as splitFileName
from functools import wraps
from subprocess import call
from flask import request
from flask_api.status import HTTP_400_BAD_REQUEST
from uuid import uuid1
import json

# Local imports
from config import *


def validate_submit_search_form(callback):
    @wraps(callback)
    def validate(*args, **kwargs):
        if 'img' not in request.files:
            return BAD_REQUEST_STR('Add an image'), HTTP_400_BAD_REQUEST

        img_file = request.files['img']
        img_name = save_file(img_file)

        return callback(img_name, *args, **kwargs)
    return validate


def save_file(img):
    imgName = str(uuid1())+splitFileName(img.filename)[1]
    img.save(UPLOADED_IMGS_DIR+imgName)

    return imgName


def validate_bounding_boxes_selector_form(callback):
    @wraps(callback)
    def validate_bounding_boxes_form(*args, **kwargs):
        if 'img-name' not in request.form:
            return BAD_REQUEST_STR('Image name not found.')
        elif 'objects-data' not in request.form:
            return BAD_REQUEST_STR('No objects data found.')
        elif 'bounding-boxes-data' not in request.form:
            return BAD_REQUEST_STR('No bounding boxes data found.')

        imgName = request.form['img-name']

        objsDataStr = request.form['objects-data'].replace("'", "\'")
        objsData = json.loads(objsDataStr)

        BBsStr = request.form['bounding-boxes-data'].replace("'", "\'")
        BBs = json.loads(BBsStr)

        return callback(imgName, objsData, BBs, *args, **kwargs)
    return validate_bounding_boxes_form


def BAD_REQUEST_STR(msj=''):
    return f'<h1>Bad request</h1><p>{msj}</p>'
