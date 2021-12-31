import os
import datetime
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .figures import graph
from .models import Item, ItemHistory, User

USER_INVENTORY = '/userInventory'


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


@login_required(login_url='/login')
def user_logout(request):
    """User Logout request.

    Args:
        request ([type]): HTTP Request.

    Returns:
        HttpResponseRedirect : baseHome.html
    """
    clear_graph_history(request.user)
    logout(request)
    return HttpResponseRedirect('/')


def user_signup(request):
    username = password = email = ''
    SIGNUP_PAGE = 'home/signup.html'
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        password = make_password(request.POST['password'])
        does_user_exist = User.objects.filter(username=username).exists()
        does_email_exist = User.objects.filter(email=email).exists()
        if does_user_exist and does_email_exist:
            return render(request, SIGNUP_PAGE,
                          {"error": "Invalid Sign-up! Username and Email are already taken."})
        elif does_user_exist:
            return render(request, SIGNUP_PAGE,
                          {"error": "Invalid Sign-up! Username already taken."})
        elif does_email_exist:
            return render(request, SIGNUP_PAGE,
                          {"error": "Invalid Sign-up! Email already taken."})
        else:
            new_user = User(username=username, email=email, password=password)
            new_user.save()
            return HttpResponseRedirect('/home')
    return render(request, SIGNUP_PAGE)


@login_required(login_url='/login')
def user_landing_page(request):
    """User Homepage

    Args:
        request ([type]): Http Request.

    Returns:
        [type]: userHome.html with username.
    """
    clear_graph_history(request.user)
    return render(request, 'home/userHome.html', {"username": str(request.user).title(),})


@login_required(login_url='/login')
def create_item(request):
    """Inventory Home Page.

    Args:
        request ([type]): HTTP request.
        item_id (int, optional): Item ID number, if specified. Defaults to 0.

    Returns:
        [type]: userHomeInventory.html with username, item, items, and itemHistory.
    """
    if request.POST:
        item = Item.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            user_visibility=f'{request.user},',
            quantity=request.POST.get('quantity'))
        item.save()
        return HttpResponseRedirect(USER_INVENTORY)

    clear_graph_history(request.user)
    items = Item.objects.all().select_related()
    return render(request, 'home/userHomeInventoryCreate.html',
                  {"username": str(request.user).title(), "items": items,})


@login_required(login_url='/login')
def delete_item(request, item_id=0):
    """Inventory Home Page.

    Args:
        request ([type]): HTTP request.
        item_id (int, optional): Item ID number, if specified. Defaults to 0.

    Returns:
        [type]: userHomeInventory.html with username, item, items, and itemHistory.
    """
    does_item_exist = Item.objects.filter(id=item_id).exists()
    does_item_history_exist = ItemHistory.objects.filter(
        item_id=item_id).exists()
    user_owns = request.user in Item.objects.get(
        id=item_id).user_visibility.split(',')
    if does_item_exist and user_owns:
        item_to_delete = Item.objects.get(id=item_id)
        item_to_delete.delete()
        if does_item_history_exist:
            item_history_delete = ItemHistory.objects.filter(
                item_id=item_id).select_related()
            item_history_delete.delete()
        return HttpResponseRedirect(USER_INVENTORY)
    else:
        return HttpResponseRedirect(USER_INVENTORY)


@login_required(login_url='/login')
def user_inventory(request, item_id=0, item_range=10):
    """Creates an inventory item.

    Args:
        request ([type]): HTTP request.

    Returns:
    Returns:
        [type]: userHomeInventory.html with username, item, items, and item_history.
    """
    clear_graph_history(request.user)
    if (request.POST.get('search')):
        items = Item.objects.filter(
            name__contains=request.POST['search'], user_visibility__contains=f'{request.user},').select_related()

    else:
        items = Item.objects.filter(id__range=((item_range - 10), item_range),
                                    user_visibility__contains=f'{request.user},').select_related()
    item = str()
    item_history = str()
    if item_id != 0:
        item = Item.objects.get(id=item_id)
        item_history = ItemHistory.objects.filter(
            item_id=item_id).select_related()
    return render(request, 'home/userHomeInventory.html',
                  {"username": str(request.user).title(), "item": item, "items": items, "itemHistories": item_history,
                   'item_range': item_range, 'item_id': item_id,})


@login_required(login_url='/login')
def user_inventory_edit(request, item_id=0, item_range=10):
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
            new_history = ItemHistory(item_id=item, date_of_change=datetime.now(), price_before=item.price,
                                      price_after=request.POST.get('price'), quantity_before=item.quantity,
                                      quantity_after=request.POST.get('quantity'))
            new_history.save()
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.price = request.POST['price']
        item.quantity = request.POST.get('quantity')
        item.save()
        return HttpResponseRedirect(USER_INVENTORY)
    items = Item.objects.filter(id__range=(
        (item_range - 10), item_range), user_visibility__contains=f'{request.user},').select_related()
    item_history = ItemHistory.objects.filter(item_id=item).select_related()
    return render(request, 'home/userHomeInventoryEdit.html',
                  {"username": str(request.user).title(), "item": item, "items": items,
                   "itemHistories": item_history, "item_range": item_range, "item_id": item_id, "inventory": True})


@login_required(login_url='/login')
def user_insights(request, item_id=0, item_range=10):
    """Inventory Insights Home page.

    Args:
        item_id: item id number.
        request ([type]): HTTP Request.

    Returns:
        [type]: userHomeInsights.html
    """
    items = Item.objects.filter(id__range=(
        (item_range - 10), item_range), user_visibility__contains=f'{request.user},').select_related()
    if item_id != 0:
        item = Item.objects.get(id=item_id)
        if request.POST:
            start_date_query = request.POST['startDate'].split('-')
            end_date_query = request.POST['endDate'].split('-')
            start_date = datetime.datetime(int(start_date_query[0]), int(
                start_date_query[1]), int(start_date_query[2]))
            end_date = datetime.datetime(int(end_date_query[0]), int(
                end_date_query[1]), int(end_date_query[2]))
            if (start_date < end_date):
                item_history = ItemHistory.objects.filter(
                    item_id=item, date_of_change__gte=start_date, date_of_change__lte=end_date)
            else:
                item_history = ItemHistory.objects.filter(
                    item_id=item).select_related()
        else:
            item_history = ItemHistory.objects.filter(
                item_id=item).select_related()
        price_graph = quantity_graph = ''
        if len(item_history) > 1:
            date_change = [x.date_of_change.strftime(
                '%m-%d %I:%M %p') for x in item_history if x.date_of_change]
            price_graph = f"home/temp/{request.user}/" + str(graph(
                date_change,
                [y.price_after for y in item_history
                 if y.price_after], str(request.user), True))
            quantity_graph = f"home/temp/{request.user}/" + str(graph(
                date_change,
                [y.quantity_after for y in item_history if
                 y.quantity_after], str(request.user), False))

        return render(request, 'home/userHomeInsights.html', {"username": str(request.user).title(),
                                                              "items": items,
                                                              "price_graph": price_graph,
                                                              "quantity_graph": quantity_graph,
                                                              "item": item,
                                                              "item_id": item_id, "item_range": item_range,})
    return render(request, 'home/userHomeInsights.html',
                  {"username": str(request.user).title(), "items": items, "item_id": item_id,
                   "item_range": item_range,})


@login_required(login_url='/login')
def user_users(request):
    return render(request, 'home/userHomeUsers.html', {"username": str(request.user).title(),})


def clear_graph_history(username):
    path = os.path.join(os.path.dirname(__file__), 'static',
                        'home', 'temp', f'{username}')
    if os.path.exists(path):
        os.chdir(path)
        for file in os.listdir(path):
            os.remove(file)
