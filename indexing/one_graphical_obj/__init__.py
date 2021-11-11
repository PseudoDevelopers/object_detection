from .graphical import process as process_graphical
from .index import index_data

from ..index_for import IndexFor


def process_and_index(obj, BBs, imgName, indexFor=IndexFor.onlySubmit):
    processedGraphicalObj = process_graphical(obj)
    indexed = index_data(processedGraphicalObj, BBs, imgName, indexFor=indexFor)

    return indexed
