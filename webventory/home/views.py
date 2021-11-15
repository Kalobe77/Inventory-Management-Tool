from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Item, ItemHistory
from .forms import ItemForm


# Create your views here.
def home(request):
    return render(request, 'home/baseHome.html')


def user_login(request):
    if (request.user.is_authenticated):
        return HttpResponseRedirect('/userHome')
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/userHome')
        else:
            return render(request, 'home/login.html',
                          {"error": "Invalid Login! Please check your username and/or password."})
    return render(request, 'home/login.html')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def user_landing_page(request):
    return render(request, 'home/userHome.html', {"username": str(request.user).title()})


@login_required(login_url='/login')
def user_inventory(request, item_id=0):
    items = Item.objects.all()
    item = str()
    itemHistory = str()
    if item_id != 0:
        item = Item.objects.get(id=item_id)
        itemHistory = ItemHistory.objects.filter(item_id=item)
    return render(request, 'home/userHomeInventory.html',
                  {"username": str(request.user).title(), "item": item, "items": items, "itemHistories": itemHistory})


@login_required(login_url='/login')
def user_inventory_edit(request, item_id=0):
    item = Item.objects.get(id=item_id)
    if request.POST:
        if ((request.POST['price'] != str(item.price)) or (request.POST['quantity'] != str(item.quantity))):
            newHistory = ItemHistory(item_id=item, date_of_change=datetime.now(), price_before=item.price,
                                     price_after=request.POST.get('price'), quantity_before=item.quantity,
                                     quantity_after=request.POST.get('quantity'))
            newHistory.save()
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.price = request.POST['price']
        item.user_visibility = request.POST['user_visibility']
        item.quantity = request.POST.get('quantity')
        item.save()
        return HttpResponseRedirect('/userInventory')
    items = Item.objects.all()
    itemHistory = ItemHistory.objects.filter(item_id=item)
    return render(request, 'home/userHomeInventoryEdit.html',
                  {"username": str(request.user).title(), "item": item, "items": items, "form": ItemForm,
                   "itemHistories": itemHistory})


@login_required(login_url='/login')
def user_insights(request):
    return render(request, 'home/userHomeInsights.html', {"username": str(request.user).title()})
