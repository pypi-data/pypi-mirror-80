def groupby_items(items, field):
    from operator import itemgetter
    from itertools import groupby
    groupby_result = {}
    for k, v in groupby(items, key=itemgetter(field)):
        groupby_result[k] = list(v)
    return groupby_result
