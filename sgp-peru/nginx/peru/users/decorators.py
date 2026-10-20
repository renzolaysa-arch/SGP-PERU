from multiprocessing.dummy import Array
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

def check_user(groups: list, url):
    def decorator(function):
        @never_cache
        @wraps(function)
        def wrapper(request, *args, **kwargs):
            correct = False
            for group in groups:
                if request.user.groups.filter(name=group).exists():
                    correct = True

            if correct:
                return function(request, *args, **kwargs)
            else:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse(
                        {'error': 'session_expired' if not request.user.is_authenticated else 'permission_denied',
                         'login_url': reverse(url)},
                        status=401 if not request.user.is_authenticated else 403,
                    )
                return HttpResponseRedirect(reverse(url))

        return wrapper

    return decorator
