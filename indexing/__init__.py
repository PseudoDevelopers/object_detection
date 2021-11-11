from .zero_graphical_objs import process_and_index as process_and_index_zero_graphical_objs
from .one_graphical_obj import process_and_index as process_and_index_one_graphical_obj
from .two_graphical_objs import process_and_index as process_and_index_two_graphical_objs
from .more_than_two_graphical_objs import process_and_index as process_and_index_more_than_two_graphical_objs

from .index_for import IndexFor

from logger import log
_LOGGER = log(__name__)


def process_and_index(graphicalObjs, BBs, imgName):
    """
    Index the data for Database submit
    """
    indexedData = None
    
    if len(graphicalObjs) == 0:
        indexedData = process_and_index_zero_graphical_objs(BBs, imgName)
    elif len(graphicalObjs) == 1:
        indexedData = process_and_index_one_graphical_obj(graphicalObjs[0], BBs, imgName)
    elif len(graphicalObjs) == 2:
        indexedData = process_and_index_two_graphical_objs(graphicalObjs, BBs, imgName)
    else:
        indexedData = process_and_index_more_than_two_graphical_objs(graphicalObjs, BBs, imgName)

    _LOGGER.info('Data has been indexed for submitting')
    return indexedData


def process_and_index_for_submit_search(graphicalObjs, BBs, imgName):
    """
    Index the data for searching
    """
    indexedForSubmit, dataForSearch = None, None
    
    if len(graphicalObjs) == 0:
        indexedForSubmit, dataForSearch = process_and_index_zero_graphical_objs(BBs, imgName, indexFor=IndexFor.bothSubmitSearch)
    elif len(graphicalObjs) == 1:
        indexedForSubmit, dataForSearch = process_and_index_one_graphical_obj(graphicalObjs[0], BBs, imgName, indexFor=IndexFor.bothSubmitSearch)
    elif len(graphicalObjs) == 2:
        indexedForSubmit, dataForSearch = process_and_index_two_graphical_objs(graphicalObjs, BBs, imgName, indexFor=IndexFor.bothSubmitSearch)
    else:
        indexedForSubmit, dataForSearch = process_and_index_more_than_two_graphical_objs(graphicalObjs, BBs, imgName, indexFor=IndexFor.bothSubmitSearch)

    _LOGGER.info('Data has been indexed for searching')
    return indexedForSubmit, dataForSearch
