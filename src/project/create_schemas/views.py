from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SchemaForm, TypeDataFormSet,  SchemaForm2
from .for_views import *
from proj.utils import collection


@login_required
def new_schema(request):
    if request.method == 'POST':
        form = SchemaForm(request.POST)
        formset = TypeDataFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            parent = datajson(form, formset)
            collection.insert_one(parent)
            return redirect(f'edit/{parent["_id"]}/')
        else:
            context = {
                "form": form,
                "formset": formset,
                "message": 'Your data is invalid',
                "integer": "integer",
                "schema": "New Schema"
            }
            return render(request, "new_schema.html", context)
    else:
        form = SchemaForm()
        formset = TypeDataFormSet()
        context = {
            "form": form,
            "formset": formset,
            "integer": "integer",
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
def edit_schema(request, _id):
    if request.method == 'POST':
        form = SchemaForm2(request.POST)
        formset = TypeDataFormSet(request.POST)
        context = {
            "form": form,
            "formset": formset,
            "integer": "integer",
            "schema": "Edit Schema"
        }
        if form.is_valid() and formset.is_valid():
            parent = datajson(form, formset)
            validation_name = collection.find_one({"_id": ObjectId(_id)})
            validation_name2 = collection.find_one({"name": parent["name"]})
            if validation_name2:
                if validation_name["_id"] != validation_name2["_id"]:
                    context["message"] = "Wrong name. Choice another name"
                else:
                    collection.replace_one({"_id": ObjectId(_id)}, parent)
                    formset2 = TypeDataFormSet(initial=parent["schema"])
                    context["formset"] = formset2
            else:
                collection.replace_one({"_id": ObjectId(_id)}, parent)
                formset2 = TypeDataFormSet(initial=parent["schema"])
                context["formset"] = formset2
        return render(request, "new_schema.html", context)
    else:
        dataset = datajson_for_initial(_id)
        form = SchemaForm(initial=dataset)
        formset = TypeDataFormSet(initial=dataset["schema"])
        context = {
            "form": form,
            "formset": formset,
            "integer": "integer",
            "schema": "Edit Schema"
        }
        return render(request, "new_schema.html", context)


@login_required
def delete_column(request, _id, id_child):
    dataset = datajson_for_delete_column(_id, id_child)
    collection.replace_one({"_id": ObjectId(_id)}, dataset)
    return redirect(edit_schema, _id=_id)
