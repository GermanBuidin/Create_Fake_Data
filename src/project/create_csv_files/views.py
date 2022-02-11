from bson import ObjectId
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .tasks import start_create_files
from .forms import NumberRows
from .for_views import list_object, list_for_download
from proj.utils import collection



@login_required
def data_sets(request):
    data_set = list_object()
    context = {
        "sets": data_set
    }
    return render(request, "data_sets.html", context)


@login_required
def data_schemas(request):
    data_sets_ = list_for_download()
    if request.method == 'POST':
        form = NumberRows(request.POST)
        if form.is_valid():
            data = form.clean()
            print(data['rows'])
            start_create_files.delay(data['rows'])
            return redirect("load")

    form = NumberRows()
    context = {
        "form": form,
        "data": data_sets_
    }
    return render(request, "data_schema.html", context)


@login_required
def del_schema(request, idd):
    collection.delete_one({'_id': ObjectId(idd)})
    return redirect('sets')
