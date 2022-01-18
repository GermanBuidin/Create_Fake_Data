from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .tasks import *


def new_schema(request):
    print(get_number.delay(x=5, y=6))
    print (10)
    return render(request, "new_schema.html")


def data_schemas(request):
    return render(request, "data_schema.html")


def data_sets(request):
    return render(request, "data_sets.html")


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