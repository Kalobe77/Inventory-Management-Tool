from django.http import HttpResponseRedirect


def is_logged_in(view_function):
    """Redirects to home if logged in, else goes to login page"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/userHome')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper
