from functools import wraps
from django.shortcuts import redirect
from django.http import HttpRequest
from rest_framework.response import Response

def login_require(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Check if user is authenticated by verifying the session
        if 'admin_data' not in request.session:
            # Redirect to the login page if not authenticated
            return redirect('adminindex')
        # If authenticated, proceed with the view
        return view_func(request, *args, **kwargs)
    return wrapped_view
