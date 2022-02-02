from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, SchemaForm, TypeDataFormSet, TypeDataForm
from .tasks import *
from .for_views import *
from proj.utils import collection


def data_sets(request):
    print(get_number.delay(x=5, y=6))
    print(10)
    return render(request, "new_schema.html")


def data_schemas(request):
    return render(request, "data_schema.html")


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
                "message": 'Your data is invalid'
            }
            return render(request, "new_schema.html", context)
    else:
        form = SchemaForm()
        TypeDataFormSetEmpty = formset_factory(TypeDataForm, extra=1)
        formset = TypeDataFormSetEmpty()
        context = {
            "form": form,
            "formset": formset,
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
        dataset = datajson_for_initial(_id)
        form = SchemaForm(request.POST)
        formset = TypeDataFormSet(request.POST)
        context = {
            "form": form,
            "formset": formset,
            "number": dataset[0]["schema"]
        }
        if form.is_valid() and formset.is_valid():
            parent = datajson(form, formset)
            collection.replace_one({"_id": ObjectId(_id)}, parent)
            context["number"] = parent["schema"]
        return render(request, "new_schema.html", context)
    else:
        dataset = datajson_for_initial(_id)
        data_initial = datajson_for_initial_formset(dataset[0]["schema"])
        form = SchemaForm(initial=dataset[0])
        formset = TypeDataFormSet(initial=data_initial)
        context = {
            "form": form,
            "formset": formset,
            "number": dataset[0]["schema"]
        }
        return render(request, "new_schema.html", context)


@login_required
def delete_column(request, _id, id_child):
    dataset = datajson_for_delete_column(_id, id_child)
    collection.replace_one({"_id": ObjectId(_id)}, dataset)
    return redirect(edit_schema, _id=_id)
