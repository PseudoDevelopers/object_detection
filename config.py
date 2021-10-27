"""
This file contains some of the most commonly used constants in the project.
"""


# If this is true then you can show logs in console
# And popups showing detected objects & texts
GLOBAL_DEBUG = True


UPLOADED_IMGS_DIR = 'static/images/client/'
INDEXED_IMGS_DIR = 'images/indexed/'


OPEN_CV_MIN_THRESHOLD = 0.5     # Out of 1
OCR_MIN_THRESHOLD = 80          # Out of 100


MONGO = {
    'dbUrl': 'mongodb://localhost:27017',
    'client': 'image-based-search-engine',
    'collection': 'indexed-data'
}
