from typing import Union, Callable, Any
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render


def is_logged_in(view_function: Callable[[HttpRequest, Any], Union[render, HttpResponseRedirect]]) -> Callable[[HttpRequest, Any], Union[render, HttpResponseRedirect]]:
    """
    is_logged_in Redirects to home if logged in, else goes to login page
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/userHome')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper
