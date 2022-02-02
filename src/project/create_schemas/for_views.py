from bson import ObjectId
from proj.utils import collection


def datajson(form: 'form', formset: "formset"):
    parent = form.clean()
    child = []
    for f in formset:
        child.append({f.prefix: f.clean()})
    parent['schema'] = child
    return parent


def datajson_for_initial(_id):
    dataset = list(collection.find({"_id": ObjectId(_id)}, {"_id": False}))
    data = []
    for i, n in enumerate(dataset[0]["schema"]):
        for key, value in n.items():
            data.append({f"form-{i}": value})
    dataset[0]["schema"] = data
    return dataset


def datajson_for_delete_column(_id, id_child):
    dataset = list(collection.find({"_id": ObjectId(_id)}, {"_id": False}))
    dataset = dataset[0]
    for i in dataset["schema"]:
        if id_child in i:
            dataset["schema"].remove(i)
    return dataset


def datajson_for_initial_formset(data):
    data_initial = []
    for n in data:
        for value in n.values():
            data_initial.append(value)
    return data_initial
