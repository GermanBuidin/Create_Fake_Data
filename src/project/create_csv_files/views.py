from bson import ObjectId
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .tasks import *
from proj.utils import collection


def data_sets(request):
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

    context = {
        "sets": data_set
    }
    return render(request, "data_sets.html", context)


def data_schemas(request):
    return render(request, "data_schema.html")


def delSchema(idd):
    print(idd)
    return HttpResponse('Hello')


