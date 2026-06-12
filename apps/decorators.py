from functools import wraps
from django.shortcuts import redirect

def seller_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('adminlogin')

        if not getattr(request.user, "is_seller", False):
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return wrapper


from functools import wraps

def customer_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        customer_id = request.session.get("customer_id")

        if not customer_id:
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper