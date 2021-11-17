from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Item, ItemHistory


# Create your views here.
def home(request):
    """Webventory Homepage

    Args:
        request ([type]): HTTP Request

    Returns:
        render: Homepage.
    """
    return render(request, 'home/baseHome.html')


def user_login(request):
    """User Login page

    Args:
        request ([type]): HTTP Request

    Returns:
        [type]: login.html
    """
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
    """User Logout request.

    Args:
        request ([type]): HTTP Request.

    Returns:
        HttpResponseRedirect : baseHome.html
    """
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/login')
def user_landing_page(request):
    """User Homepage

    Args:
        request ([type]): Http Request.

    Returns:
        [type]: userHome.html with username.
    """
    return render(request, 'home/userHome.html', {"username": str(request.user).title()})


@login_required(login_url='/login')
def user_inventory(request, item_id=0):
    """Inventory Home Page.

    Args:
        request ([type]): HTTP request.
        item_id (int, optional): Item ID number, if specified. Defaults to 0.

    Returns:
        [type]: userHomeInventory.html with username, item, items, and itemHistory.
    """
    items = Item.objects.all().select_related()
    item = str()
    itemHistory = str()
    if item_id != 0:
        item = Item.objects.get(id=item_id)
        itemHistory = ItemHistory.objects.filter(item_id=item).select_related()
    return render(request, 'home/userHomeInventory.html',
                  {"username": str(request.user).title(), "item": item, "items": items, "itemHistories": itemHistory})


@login_required(login_url='/login')
def user_inventory_edit(request, item_id=0):
    """Inventory edit page.

    Args:
        request ([type]): HTTP request.
        item_id (int, optional): Item ID number, if specified. Defaults to 0.

    Returns:
        [type]: HTTPResponseRedirect to Inventory Home page if form submitted, 
        otherwise, Renders Inventory Edit page.
    """
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
    items = Item.objects.all().select_related()
    itemHistory = ItemHistory.objects.filter(item_id=item)
    return render(request, 'home/userHomeInventoryEdit.html',
                  {"username": str(request.user).title(), "item": item, "items": items,
                   "itemHistories": itemHistory})


@login_required(login_url='/login')
def user_insights(request):
    """Inventory Insights Home page.

    Args:
        request ([type]): HTTP Request.

    Returns:
        [type]: userHomeInsights.html
    """
    return render(request, 'home/userHomeInsights.html', {"username": str(request.user).title()})
