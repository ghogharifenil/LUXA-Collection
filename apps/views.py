from .forms import ProductForm
from .models import Product
from django.shortcuts import render, redirect
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode

def luxa(request):
    return render(request, "html/luxa.html")


def home(request):
    return render(request, "html/home.html")


def collection_department(request):
    return render(request, "html/collection_department.html")


def add_product(request):

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect('add_product')

    else:
        form = ProductForm()

    return render(
        request,
        'admin/addpro.html',{'form': form})


def detail(request , name):
    product = get_object_or_404(Product , name=name)
    return render(request , "html/product_detail.html",{"product": product })
    

def adminuser(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("email")

    user = authenticate(request,email = email , password = password)

    if user is not None and user.is_seller:
        auth_login(request,user)
        return redirect("/deshboard/")
    return render(request , "admin/adminlogin.html")


def dashboard(request):
    products = Product.objects.all() 
    return render(request , 'admin/dashboard.html',{"products":products})


def viewpro(request):
    return render(request, "admin/viewproduct.html")

# --------------------------------------------------------------
# ---------------------  Product -------------------------------
# --------------------------------------------------------------

def dress(request):
    products = Product.objects.filter(
        category='Dress'
    )
    return render(
        request,
        'products/dress.html',{'products': products})


def footwear(request):

    products = Product.objects.filter(
        category='Footwear'
    )
    return render(
        request,
        'products/footwear.html',{'products': products})


def heals(request):
    products = Product.objects.filter(
        category='Heals'
    )
    return render(
        request,
        'products/heals.html',{'products': products})


def jwelery(request):
    products = Product.objects.filter(
        category='Jwelery'
    )
    return render(
        request,
        'products/jwelery.html',
        {
            'products': products
        }
    )


def pent(request):
    products = Product.objects.filter(
        category='Pent'
    )
    return render(
        request,
        'products/pent.html',
        {
            'products': products
        }
    )


def saree(request):
    products = Product.objects.filter(
        category='Saree'
    )
    return render(
        request,
        'products/saree.html',
        {
            'products': products
        }
    )


def shert(request):
    products = Product.objects.filter(
        category='Shert'
    )
    return render(
        request,
        'products/shert.html',
        {
            'products': products
        }
    )


def shoes(request):
    products = Product.objects.filter(
        category='Shoes'
    )
    return render(
        request,
        'products/shoes.html',
        {
            'products': products
        }
    )
# --------------------------------------------------------------
# --------------------------------------------------------------
