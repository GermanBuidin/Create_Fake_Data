from bson import ObjectId

from main_catalog.utils import collection


def select_all_schemas(user_id):
    sets = list(collection.find({'user': user_id}))
    data_set = []
    number = 1
    for i in sets:
        if isinstance(i['_id'], ObjectId):
            document_id = ObjectId(i['_id'])
            date = ObjectId(document_id).generation_time
            name = i['name']
            dataobj = f'{i["_id"]}'
            data_set.append({'id': document_id, 'date': date, 'name': name, 'number': number, 'dataobj': dataobj})
            number += 1
    return data_set


def select_for_download(user_id):
    sets = list(collection.find({'user': user_id}))
    data_set = []
    number = 1
    for i in sets:
        if isinstance(i['_id'], ObjectId):
            if 'datenow' in i:
                i['number'] = number
                data_set.append(i)
                number += 1
    return data_set


def data_cleaning(user_id):
    schema_set = list(collection.find({'user': user_id}))
    for i in schema_set:
        if isinstance(i['_id'], ObjectId):
            if 'datenow' in i:
                i['datenow'] = None
                i['status'] = None
                i['link'] = None
                collection.replace_one({"_id": ObjectId(i['_id'])}, i)
    schema_set = list(collection.find({'user': user_id}))
    data_set = []
    for i in schema_set:
        if isinstance(i['_id'], ObjectId):
            data_set.append(i)
    return data_set
