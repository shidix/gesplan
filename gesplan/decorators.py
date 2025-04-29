from django.http import JsonResponse
from django.shortcuts import render, redirect
from gesplan.commons import  show_exc



#from .common_lib import get_adviser, get_client

def group_required(*group_names):
    def _method_wrapper(f):
        def _arguments_wrapper(request, *args, **kwargs) :
            if request.user.is_authenticated:
                if bool(request.user.groups.filter(name__in=group_names)) or request.user.is_superuser:
                    return f(request, *args, **kwargs)
                else:
                    return (render(request, "error_exception.html", {'exc':"This user have not permission to access to this section"}))
            else:
                return redirect('auth_login')
        return _arguments_wrapper
    return _method_wrapper

def group_required_pwa(*group_names):
    def _method_wrapper(f):
        def _arguments_wrapper(request, *args, **kwargs) :
            if request.user.is_authenticated:
                if bool(request.user.groups.filter(name__in=group_names)):
                    return f(request, *args, **kwargs)
                else:
                    return (render(request, "error_exception.html", {'exc':"This user have not permission to access to this section"}))
            return redirect('pwa-login')
        return _arguments_wrapper
    return _method_wrapper

def group_required_json(*group_names):
    def _method_wrapper(f):
        def _arguments_wrapper(request, *args, **kwargs) :
            try:
                if request.user.is_authenticated:
                    if bool(request.user.groups.filter(name__in=group_names)):
                        return f(request, *args, **kwargs)
                    else:
                        return JsonResponse({'error':"This user have not permission to access to this section"})
                return JsonResponse({'error':"This user have not permission to access to this section"})
            except Exception as e:
                print(show_exc(e))
                return JsonResponse({'error':"This user have not permission to access to this section"})
        return _arguments_wrapper
    return _method_wrapper

