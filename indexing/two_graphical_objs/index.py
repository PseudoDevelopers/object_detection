from math import ceil

from ..index_for import IndexFor

from DB.schema import *


def index_data(graphicalObjs, BBs, imgName, indexFor):
    nthAngleObj = str(ceil(graphicalObjs['angle'] / ANGLE_RATIO_RANGE))
    nthDistanceRatioObj = str(ceil(graphicalObjs['distanceRatio'] / DISTANCE_RATIO_RANGE))

    if indexFor == IndexFor.onlySubmit:
        return index_for_submit(nthAngleObj, nthDistanceRatioObj, BBs, imgName)

    elif indexFor == IndexFor.bothSubmitSearch:
        indexedForSubmit = index_for_submit(nthAngleObj, nthDistanceRatioObj, BBs, imgName)
        dataForSearch = index_for_search(nthAngleObj, nthDistanceRatioObj, BBs)

        return indexedForSubmit, dataForSearch


def index_for_submit(nthAngleObj, nthDistanceRatioObj, BBs, imgName):
    return {
        f'2.{nthAngleObj}.{nthDistanceRatioObj}.{len(BBs["SBBs"])}.{len(BBs["DBBs"])}': {
            'SBBs': BBs['SBBs'],
            'DBBs': BBs['DBBs'],
            'img': imgName
        }
    }


def index_for_search(nthAngleObj, nthDistanceRatioObj, BBs):
    noOfSBBs = str(len(BBs["SBBs"]))
    noOfDBBs = str(len(BBs["DBBs"]))

    query = {
        '_id': 1,
        f'2.{nthAngleObj}.{nthDistanceRatioObj}.{noOfSBBs}.{noOfDBBs}': {
            '$elemMatch': {
                'SBBs': BBs['SBBs']
            }
        }
    }

    filterFields = {
        '_id': 0,
        f'2.{nthAngleObj}.{nthDistanceRatioObj}.{noOfSBBs}.{noOfDBBs}': {
            'DBBs': 1,
            'img': 1
        }
    }

    def retriveData(obj):
        return obj\
            .get('2', {})\
            .get(nthAngleObj, {})\
            .get(nthDistanceRatioObj, {})\
            .get(noOfSBBs, {})\
            .get(noOfDBBs, None)

    return {
        'query': query,
        'filterFields': filterFields,
        'retriveData': retriveData
    }
