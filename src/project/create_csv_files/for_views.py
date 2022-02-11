from bson import ObjectId

from proj.utils import collection


def list_object():
    sets = list(collection.find())
    data_set = []
    number = 1
    for i in sets:
        if isinstance(i['_id'], ObjectId):
            idd = ObjectId(i['_id'])
            date = ObjectId(idd).generation_time
            name = i['name']
            dataobj = f'{i["_id"]}'
            data_set.append({'id': idd, 'date': date, 'name': name, 'number': number, 'dataobj': dataobj})
            number += 1
    return data_set


def list_for_download():
    sets = list(collection.find())
    data_set = []
    number = 1
    for i in sets:
        if isinstance(i['_id'], ObjectId):
            if 'datenow' in i:
                i['number'] = number
                data_set.append(i)
                number += 1
    return data_set


def list_cleaner():
    sets = list(collection.find())
    for i in sets:
        if isinstance(i['_id'], ObjectId):
            if 'datenow' in i:
                i['datenow'] = None
                i['processing'] = None
                i['color'] = None
                i['link'] = None
                collection.replace_one({"_id": ObjectId(i['_id'])}, i)
    sets = list(collection.find())
    data_set = []
    for i in sets:
        if isinstance(i['_id'], ObjectId):
            data_set.append(i)
    return data_set

