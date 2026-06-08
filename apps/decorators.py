from django.shortcuts import redirect


# --------------------+ Admin Ke Liye +----------------------

def seller_required(view_func):

    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('admin')

        if not request.user.is_seller:
            return redirect('home')

        return view_func(request, *args, **kwargs)

    return wrapper

# --------------------+ Customer Ke Liye +----------------------



def customer_login_required(view_func):

    def wrapper(request, *args, **kwargs):

        if "customer_id" not in request.session:
            return redirect("login")

        return view_func(request, *args, **kwargs)

    return wrapper