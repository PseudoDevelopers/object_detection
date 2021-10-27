from DB import read_from_db


def search_from_db(dataForSearch):
    result = read_from_db(dataForSearch['query'], dataForSearch['filterFields'])

    imgs = dataForSearch['retriveData'](result)
    if imgs == None:
        return []

    # TODO: Match for DBBs
    imgs = [img['img'] for img in imgs]

    return imgs
