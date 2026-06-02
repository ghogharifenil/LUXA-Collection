from .forms import ProductForm
from .models import Product
from django.shortcuts import render, redirect
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

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
        'html/addpro.html',{'form': form})

def detail(request , name):
    product = get_object_or_404(Product , name=name)

    return render(request , "html/product_detail.html",{"product": product })
    

def adminuser(request):
    if request.method == 'POST':
        email = request.POST("email")
        password = request.POST("email")

    user.at

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
