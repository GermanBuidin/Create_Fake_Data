from bson import ObjectId
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .tasks import start_create_files
from .forms import NumberRows
from .for_views import select_all_schemas, select_for_download
from main_catalog.utils import collection
from .create_file import create_files

@login_required
def list_schemas(request):
    user_id = request.user.id
    data_set = select_all_schemas(user_id)
    context = {
        "sets": data_set
    }
    return render(request, "list_schemas.html", context)


@login_required
def download_files(request):
    user_id = request.user.id
    data_sets_ = select_for_download(user_id)
    if request.method == 'POST':
        form = NumberRows(request.POST)
        if form.is_valid():
            data = form.clean()

            start_create_files.delay(user_id, data['rows'])
            return redirect("load")

    form = NumberRows()
    context = {
        "form": form,
        "data": data_sets_
    }
    return render(request, "download_files.html", context)


@login_required
def del_schema(request, document_id):
    collection.delete_one({'_id': ObjectId(document_id)})
    return redirect('sets')
