from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def home(request):
    return render(request, 'home/baseHome.html')


def user_login(request):
    username = password = ''
    if(request.user.is_authenticated):
        return HttpResponseRedirect('/userHome')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate( username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/userHome')
        else:
            return render(request, 'home/login.html', {"error": "Invalid Login! Please check your username and/or password."})
    return render(request, 'home/login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required(login_url='/login')
def user_landing_page(request):
    return render(request, 'home/userHome.html', {"username": request.user})
