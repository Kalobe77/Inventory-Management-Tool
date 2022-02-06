import datetime
import os
import re
from datetime import date
from typing import List, Union

import numpy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render

from .decorators import is_logged_in
from .figures import graph
from .models import Item, ItemHistory, User

USER_INVENTORY = '/userInventory'


# Create your views here.
@is_logged_in
def home(request: HttpRequest) -> render:
    """Webventory Homepage

    Args:
        request (HttpRequest): HTTP Request

    Returns:
        render: Homepage.
    """
    return render(request, 'home/baseHome.html')


@is_logged_in
def user_login(request: HttpRequest) -> render:
    """User Login page

    Args:
        request (HttpRequest): HTTP Request

    Returns:
        (render): login.html
    """
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
def user_logout(request: HttpRequest) -> HttpResponseRedirect:
    """User Logout request.

    Args:
        request (HttpRequest): HTTP Request.

    Returns:
        HttpResponseRedirect : baseHome.html
    """
    clear_graph_history(request.user)
    logout(request)
    return HttpResponseRedirect('/')


@is_logged_in
def user_signup(request: HttpRequest) -> Union[render, HttpResponseRedirect]:
    """
    user_signup User signup page.

    Args:
        request (HttpRequest): HTTP Request.

    Returns:
        Union[render, HttpResponseRedirect] : Render or redirect depending on the request.
    """
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
            new_user = User(
                username=username, email=email, password=password)
            new_user.save()
            return HttpResponseRedirect('/home')
    return render(request, SIGNUP_PAGE)


@login_required(login_url='/login')
def user_landing_page(request: HttpRequest) -> render:
    """User Homepage

    Args:
        request (HttpRequest): Http Request.

    Returns:
        [type]: userHome.html with username.
    """
    clear_graph_history(request.user)
    return render(request, 'home/userHome.html', {"username": str(request.user).title(), })


@login_required(login_url='/login')
def create_item(request: HttpRequest) -> Union[render, HttpResponseRedirect]:
    """Inventory Home Page.

    Args:
        request (HttpRequest): HTTP request.
        item_id (int, optional): Item ID number, if specified. Defaults to 0.

    Returns:
        Union[render, HttpResponseRedirect] : userHomeInventory.html with username, item, items, and itemHistory.
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
                  {"username": str(request.user).title(), "items": items, })


@login_required(login_url='/login')
def delete_item(request: HttpRequest, item_id=0) -> HttpResponseRedirect:
    """Inventory Home Page.

    Args:
        request (HttpRequest): HTTP request.
        item_id (int, optional): Item ID number, if specified. Defaults to 0.

    Returns:
        [type]: userHomeInventory.html with username, item, items, and itemHistory.
    """
    does_item_exist = Item.objects.filter(id=item_id).exists()
    does_item_history_exist = ItemHistory.objects.filter(
        item_id=item_id).exists()
    user_owns: List[str] = request.user in Item.objects.get(
        id=item_id).user_visibility.split(',')
    if does_item_exist and user_owns:
        item_to_delete = Item.objects.get(id=item_id)
        item_to_delete.delete()
        if does_item_history_exist:
            item_history_delete = ItemHistory.objects.filter(
                item_id=item_id).select_related()
            item_history_delete.delete()
    return HttpResponseRedirect(USER_INVENTORY)


@login_required(login_url='/login')
def user_inventory(request: HttpRequest, item_id=0, item_range=10) -> render:
    """Creates an inventory item.

    Args:
        request (HttpRequest): HTTP request.

    Returns:
        [type]: userHomeInventory.html with username, item, items, and item_history.
    """
    clear_graph_history(request.user)
    total_assets = 0
    if (request.POST.get('search')):
        items = Item.objects.filter(
            name__contains=request.POST['search'], user_visibility__contains=f'{request.user},').select_related()

    else:
        items = Item.objects.filter(id__range=((item_range - 10), item_range),
                                    user_visibility__contains=f'{request.user},').select_related()
    item_history = str()
    item = None
    total_item_worth = 0
    if item_id != 0:
        item = Item.objects.get(id=item_id)
        item_history = ItemHistory.objects.filter(
            item_id=item_id).select_related()
        total_item_worth = (item.price * item.quantity)
    for item_iter in items:
        total_assets += (item_iter.price * item_iter.quantity)
    return render(request, 'home/userHomeInventory.html',
                  {"username": str(request.user).title(), "item": item, "items": items, "itemHistories": item_history,
                   'item_range': item_range, 'item_id': item_id,
                   'total_item_worth': total_item_worth, 'total_assets': total_assets})


@login_required(login_url='/login')
def user_inventory_edit(request: HttpRequest, item_id=0, item_range=10) -> Union[render, HttpResponseRedirect]:
    """Inventory edit page.

    Args:
        request (HttpRequest): HTTP request.
        item_id (int, optional): Item ID number, if specified. Defaults to 0.
        item_range (int, optional): item range to load.

    Returns:
        Union[render, HttpResponseRedirect] : HTTPResponseRedirect to Inventory Home page if form submitted,
        otherwise, Renders Inventory Edit page.
    """

    item = Item.objects.get(id=item_id)
    if request.POST:
        if ((request.POST['price'] != str(item.price)) or (request.POST['quantity'] != str(item.quantity))):
            ItemHistory(item_id=item, date_of_change=datetime.now(), price_before=item.price,
                        price_after=request.POST.get('price'), quantity_before=item.quantity,
                        quantity_after=request.POST.get('quantity')).save()
        item.name = request.POST['name']
        item.description = request.POST['description']
        item.price = request.POST['price']
        item.quantity = request.POST.get('quantity')
        item.save()
        return HttpResponseRedirect(USER_INVENTORY)
    # filters item by range and user visibility.
    items = Item.objects.filter(id__range=(
        (item_range - 10), item_range), user_visibility__contains=f'{request.user},').select_related()
    item_history = ItemHistory.objects.filter(
        item_id=item).select_related()
    return render(request, 'home/userHomeInventoryEdit.html',
                  {"username": str(request.user).title(), "item": item, "items": items,
                   "itemHistories": item_history, "item_range": item_range, "item_id": item_id, "inventory": True})


@login_required(login_url='/login')
def user_insights(request: HttpRequest, item_id=0, item_range=10) -> render:
    """Inventory Insights Home page.

    Args:
        item_id (int): item id number.
        request (HttpRequest): request.
        item_range(int): item range to display.

    Returns:
        render : userHomeInsights.html.
    """
    # Year-Month-Day
    date_pattern = re.compile("[\d]{4}-[\d]{2}-[\d]{2}")
    items = Item.objects.filter(id__range=(
        (item_range - 10), item_range), user_visibility__contains=f'{request.user},').select_related()
    # html template variables
    return_dict = {"username": str(request.user).title(), "items": items, "item_id": item_id,
                   "item_range": item_range, }
    if item_id != 0:
        item = Item.objects.get(id=item_id)
        if request.POST and (request.POST.get('start_date_query') and request.POST.get('end_date_query')) and (date_pattern.match(request.POST.get('start_date_query')) is not None and date_pattern.match(request.POST.get('end_date_query')) is not None):
            start_date_query = request.POST['startDate'].split(
                '-')
            end_date_query = request.POST['endDate'].split('-')
            start_date = datetime.datetime(int(start_date_query[0]), int(
                start_date_query[1]), int(start_date_query[2]))
            end_date = datetime.datetime(int(end_date_query[0]), int(
                end_date_query[1]), int(end_date_query[2]))
            # if valid date range
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
        # if there is more than one item history
        if len(item_history) > 1:
            date_change: List[date] = numpy.asarray([x.date_of_change.strftime(
                '%m-%d %I:%M %p') for x in item_history if x.date_of_change])
            price_graph = f"home/temp/{request.user}/" + str(graph(
                date_change,
                numpy.asarray([y.price_after for y in item_history
                               if y.price_after]), str(request.user), True))
            quantity_graph = f"home/temp/{request.user}/" + str(graph(
                date_change,
                numpy.asarray([y.quantity_after for y in item_history if
                               y.quantity_after]), str(request.user), False))
        file_does_not_exist = False if price_graph else True
        return_dict.update({"price_graph": price_graph,
                            "quantity_graph": quantity_graph,
                            "item": item,
                            "file_does_not_exist": file_does_not_exist})
        return render(request, 'home/userHomeInsights.html', return_dict)
    return render(request, 'home/userHomeInsights.html',
                  return_dict)


@login_required(login_url='/login')
def user_users(request: HttpRequest, item_id=0, item_range=10) -> render:
    """
    user_users Change visibility settings for other users.

    Args:
        request (HttpRequest): request.
        item_id (int, optional): current item to display. Defaults to 0.
        item_range (int, optional): Range of item to display. Defaults to 10.

    Returns:
        render: page render.
    """

    item = str()
    user_visibility = str()
    item_msg = str()
    users = numpy.asarray([str(user) for user in User.objects.all()])
    if(item_id != 0):
        user_visibility = Item.objects.get(
            id=item_id).user_visibility.split(',')
        item = Item.objects.get(id=item_id)
        item_msg = item.name + " Visibility Settings"
    items = Item.objects.filter(id__range=(
        (item_range - 10), item_range), user_visibility__contains=f'{request.user},').select_related()
    return_dict = {"username": str(request.user).title(
    ), "items": items, "item_range": item_range, "users": users}
    if request.POST:
        print(request.POST)
        user_visibility_list: str = f'{user_visibility[0]},'
        for user in users:
            print(user)
            print(request.POST.get(str(user)))
            if request.POST.get(f'{user}') and f'{user}' not in user_visibility_list:
                user_visibility_list += f'{user},'
        item.user_visibility = user_visibility_list
        print(user_visibility_list)
        item.save()
        return_dict.update({"msg": "Modification Successful"})
    else:
        return_dict.update({"item_id": item_id, "item": item,
                            "msg": "Select an item to modify user visibility.", "item_msg": item_msg})
    return render(request, 'home/userHomeVisibility.html', return_dict)


def clear_graph_history(username: str) -> None:
    """
    clear_graph_history Clears Graph History.

    Args:
        username (str): username of current user.
    """
    # gets currentworking directory plus graph directory.
    path = os.path.join(os.path.dirname(__file__), 'static',
                        'home', 'temp', f'{username}')
    if os.path.exists(path):
        os.chdir(path)
        for file in os.listdir(path):
            os.remove(file)
