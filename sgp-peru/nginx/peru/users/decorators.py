from multiprocessing.dummy import Array
from django.http import HttpResponseRedirect
from django.urls import reverse

def check_user(groups: list, url):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            correct = False
            for group in groups:
                if request.user.groups.filter(name=group).exists():
                    correct = True

            if correct:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse(url))

        return wrapper

    return decorator