"""
This drops the database. And delete all indexed images.
"""

from pymongo import MongoClient
import os

# TODO: This is not working
# from config import MONGO, UPLOADED_IMGS_DIR, INDEXED_IMGS_DIR
UPLOADED_IMGS_DIR = 'static/images/client/'
INDEXED_IMGS_DIR = 'images/indexed/'

MONGO = {
    'dbUrl': 'mongodb://localhost:27017',
    'client': 'image-based-search-engine',
    'collection': 'indexed-data'
}


def drop_database():
    client = MongoClient(MONGO['dbUrl'])
    client.drop_database(MONGO['client'])


def del_indexed_imgs():
    files = os.listdir(INDEXED_IMGS_DIR)
    files.remove('.gitkeep')
    for file in files:
        os.remove(f'{INDEXED_IMGS_DIR}/{file}')


def del_uploaded_imgs():
    files = os.listdir(UPLOADED_IMGS_DIR)
    files.remove('.gitkeep')
    for file in files:
        os.remove(f'{UPLOADED_IMGS_DIR}/{file}')



if __name__ == "__main__":
    drop_database()
    del_indexed_imgs()
    del_uploaded_imgs()

    print('Project is reset!')
