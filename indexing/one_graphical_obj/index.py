from ..index_for import IndexFor

from DB.schema import *


def index_data(graphicalObj, BBs, imgName, indexFor):
    nthWidthHeightRatioObj = str(graphicalObj['widthHeightRatio'])

    if indexFor == IndexFor.onlySubmit:
        return index_for_submit(nthWidthHeightRatioObj, BBs, imgName)

    elif indexFor == IndexFor.bothSubmitSearch:
        indexedForSubmit = index_for_submit(nthWidthHeightRatioObj, BBs, imgName)
        dataForSearch = index_for_search(nthWidthHeightRatioObj, BBs)

        return indexedForSubmit, dataForSearch


def index_for_submit(nthWidthHeightRatioObj, BBs, imgName):
    return {
        f'1.{nthWidthHeightRatioObj}.{len(BBs["SBBs"])}.{len(BBs["DBBs"])}': {
            'SBBs': BBs['SBBs'],
            'DBBs': BBs['DBBs'],
            'img': imgName
        }
    }


def index_for_search(nthWidthHeightRatioObj, BBs):
    noOfSBBs = str(len(BBs["SBBs"]))
    noOfDBBs = str(len(BBs["DBBs"]))

    query = {
        '_id': 1,
        f'1.{nthWidthHeightRatioObj}.{noOfSBBs}.{noOfDBBs}': {
            '$elemMatch': {
                'SBBs': BBs['SBBs']
            }
        }
    }

    filterFields = {
        '_id': 0,
        f'1.{nthWidthHeightRatioObj}.{noOfSBBs}.{noOfDBBs}': {
            'DBBs': 1,
            'img': 1
        }
    }

    def retriveData(obj):
        return obj\
            .get('1', {})\
            .get(nthWidthHeightRatioObj, {})\
            .get(noOfSBBs, {})\
            .get(noOfDBBs, None)

    return {
        'query': query,
        'filterFields': filterFields,
        'retriveData': retriveData
    }
