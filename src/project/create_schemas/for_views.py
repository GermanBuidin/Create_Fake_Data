from bson import ObjectId
from proj.utils import collection
from django.shortcuts import redirect


def datajson(form, formset):
    parent = form.clean()
    child = []
    for i in formset.ordered_forms:
        child.append(i.clean())
    parent['schema'] = child
    return parent


def datajson_for_initial(_id):
    dataset = list(collection.find({"_id": ObjectId(_id)}, {"_id": False}))
    return dataset[0]


def datajson_for_delete_column(_id, id_child):
    if collection.find({"_id": ObjectId(_id)}):
        dataset = list(collection.find({"_id": ObjectId(_id)}, {"_id": False}))
        dataset = dataset[0]
        for i, n in enumerate(dataset["schema"]):
            if id_child == f"form-{i}":
                dataset["schema"].remove(n)
        return dataset
    else:
        return redirect("schema")


def datajson_for_initial_formset(data):
    data_initial = []
    for n in data:
        for value in n.values():
            data_initial.append(value)
    return data_initial
