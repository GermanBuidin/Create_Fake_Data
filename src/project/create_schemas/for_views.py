from bson import ObjectId
from django.shortcuts import redirect

from main_catalog.utils import collection


def create_json_date(form, formset):
    form_data = form.clean()
    formset_data = []
    for i in formset.ordered_forms:
        formset_data.append(i.clean())
    form_data['schema'] = formset_data
    return form_data


def get_initial_form_data(document_id):
    form_data = list(collection.find({"_id": ObjectId(document_id)}, {"_id": False}))
    return form_data[0]


def delete_rows(_id, id_child):
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

