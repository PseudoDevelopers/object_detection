from .graphical import process as process_graphical
from .index import index_data

from ..index_for import IndexFor


def process_and_index(objs, BBs, imgName, indexFor=IndexFor.onlySubmit):
    processedGraphicalObjs = process_graphical(objs)
    indexed = index_data(processedGraphicalObjs, BBs, imgName, indexFor=indexFor)

    return indexed
