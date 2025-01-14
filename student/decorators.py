from functools import wraps
from django.shortcuts import redirect
from django.http import HttpRequest
from rest_framework.response import Response

def login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if 'employee_data' not in request.session or 'admin_data' not in request.session :
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapped_view
