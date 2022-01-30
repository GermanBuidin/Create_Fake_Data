from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import formset_factory

from .forms import LoginForm, SchemaForm, TypeDataFormSet, SchemaFormSet
from .tasks import *
from for_views import datajson
from proj.utils import collection



def new_schema(request):
    print(get_number.delay(x=5, y=6))
    print (10)
    return render(request, "new_schema.html")


def data_schemas(request):
    return render(request, "data_schema.html")


@login_required
def data_sets(request):
    if request.method == 'POST':
        form = SchemaForm(request.POST)
        formset = TypeDataFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            parent = datajson(form, formset)
            parent['_id'] = collection.count_documents({"_id": {'$exists': True}})+1
            collection.insert_one(parent)
            return redirect(f'edit/{parent["_id"]}/')
        else:
            context = {
                "form": form,
                "formset": formset,
                "message": 'Your data is invalid'
            }
            return render(request, "data_sets.html", context)
    else:
        form = SchemaForm()
        formset = TypeDataFormSet()
        context = {
            "form": form,
            "formset": formset,
        }
        return render(request, "data_sets.html", context)


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
                    return redirect("schema")
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
def edit_schema(request, id):
    data = collection.find({'_id': id})
    dataset = [i for i in data]
    if request.method == 'POST':
        form = SchemaForm(request.POST)
        formset = TypeDataFormSet(request.POST)
        context = {
            "form": form,
            "formset": formset,
        }
        if form.is_valid() and formset.is_valid():
            parent = form.clean()
            child = []
            for f in formset:
                child.append(f.clean())
            parent['schema'] = child
            parent['_id'] = id
            collection.replace_one({"_id": id}, parent)
        return render(request, "data_sets.html", context)
    else:

        form = SchemaForm(initial=dataset[0])
        formset = TypeDataFormSet(initial=dataset[0]['schema'])
        context = {
            "form": form,
            "formset": formset,
        }
        return render(request, "data_sets.html", context)
