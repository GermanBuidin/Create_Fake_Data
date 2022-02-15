from bson import ObjectId
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SchemaFormNew, TypeDataFormSet,  SchemaFormEdit
from .for_views import create_json_date, get_initial_form_data, delete_rows
from main_catalog.utils import collection


@login_required
def create_new_schema(request):
    if request.method == 'POST':
        form = SchemaFormNew(request.POST)
        formset = TypeDataFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            schema_data = create_json_date(form, formset)
            schema_data['user'] = request.user.id
            collection.insert_one(schema_data)
            return redirect(f'edit/{schema_data["_id"]}/')
        else:
            context = {
                "form": form,
                "formset": formset,
                "message": 'Your data is invalid',
                "schema": "New Schema"
            }
            return render(request, "new_schema.html", context)
    form = SchemaFormNew()
    formset = TypeDataFormSet()
    context = {
        "form": form,
        "formset": formset,
        "schema": "New Schema"
    }
    return render(request, "new_schema.html", context)


def handler_404(request, exception):
    title = 'This page no found'
    context = {"title": title}
    return render(request, 'login.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("new_schema/")
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def edit_schema(request, document_id):
    if request.method == 'POST':

        form = SchemaFormEdit(request.POST)
        formset = TypeDataFormSet(request.POST)
        context = {
            "form": form,
            "formset": formset,
            "schema": "Edit Schema"
        }
        if form.is_valid() and formset.is_valid():
            schema_data = create_json_date(form, formset)
            schema_data['user'] = request.user.id
            validation_name = collection.find_one({"name": schema_data["name"]})
            if validation_name:
                if validation_name["_id"] != ObjectId(document_id):
                    context["message"] = "Wrong name. Choice another name"
                else:
                    collection.replace_one({"_id": ObjectId(document_id)}, schema_data)
                    formset_initial = TypeDataFormSet(initial=schema_data["schema"])
                    context['formset'] = formset_initial
            else:
                collection.replace_one({"_id": ObjectId(document_id)}, schema_data)
                formset_initial = TypeDataFormSet(initial=schema_data["schema"])
                context['formset'] = formset_initial
        return render(request, "new_schema.html", context)
    else:
        form_data = get_initial_form_data(document_id)
        form = SchemaFormNew(initial=form_data)
        formset = TypeDataFormSet(initial=form_data["schema"])
        context = {
            "form": form,
            "formset": formset,
            "schema": "Edit Schema"
        }
        return render(request, "new_schema.html", context)


@login_required
def delete_column(request, document_id, id_row):
    dataset = delete_rows(document_id, id_row)
    collection.replace_one({"_id": ObjectId(document_id)}, dataset)
    return redirect(edit_schema, document_id=document_id)
