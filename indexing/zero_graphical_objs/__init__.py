from .index import index_data

from ..index_for import IndexFor


def process_and_index(BBs, imgName, indexFor=IndexFor.onlySubmit):
    return index_data(BBs, imgName, indexFor)
