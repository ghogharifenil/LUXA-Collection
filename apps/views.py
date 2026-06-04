from .forms import ProductForm
from .models import Product
from django.shortcuts import render, redirect
from .models import Order
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from .decorators import seller_required, customer_login_required

# --------------------------------------------------------------------------------
# --------------------+ Main Page Of LUXA Collection +----------------------------
# --------------------------------------------------------------------------------


def luxa(request):
    return render(request, "html/luxa.html")

# ---------------+ Home Page +----------------------------


def home(request):
    return render(request, "html/home.html")

# ---------------+ Collection Department +----------------


def collection_department(request):
    return render(request, "html/collection_department.html")

# ---------------+ Add to Cart With Login  +----------------


@customer_login_required
def add_to_cart(request):
    return render(request, "html/add_to_cart.html")

# -----------------+ Buy with Login  +----------------------

def buy(request, name):

    product = get_object_or_404(Product, name=name)

    if request.method == "POST":

        quantity = int(request.POST.get("quantity", 1))

        total_price = product.price * quantity

        screenshot = request.FILES.get("payment_screenshot")

        Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price,
            payment_screenshot=screenshot,
            status="Pending"
        )

        return redirect("home")

    return render(
        request,
        "html/buy.html",
        {
            "product": product
        }
    )

# --------------------------------------------------------------------------------
# ------------------------+ Customer Show Detail +--------------------------------
# --------------------------------------------------------------------------------


def detail(request, name):
    product = get_object_or_404(
        Product,
        name=name
    )
    return render(
        request,
        "html/product_detail.html",
        {
            "product": product
        }
    )

# --------------------------------------------------------------
# ---------------------  Product -------------------------------
# --------------------------------------------------------------


def dress(request):

    products = Product.objects.filter(
        category='Dress'
    )
    return render(
        request,
        'products/dress.html',
        {
            'products': products
        }
    )


def footwear(request):

    products = Product.objects.filter(
        category='Footwear'
    )
    return render(
        request,
        'products/footwear.html',
        {
            'products': products
        }
    )


def heals(request):
    products = Product.objects.filter(
        category='Heals'
    )
    return render(
        request,
        'products/heals.html',
        {
            'products': products
        }
    )


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
# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                    +++++++++++++++++++++++
#                                                    +      ADMIN          +
#                                                    +++++++++++++++++++++++
# ---------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------
# ---------------------------+ Admin login +------------------------------------
# --------------------------------------------------------------------------------

# @customer_login_required
def adminuser(request):

    if request.method == 'POST':

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None and user.is_seller:
            auth_login(request, user)
            return redirect('dashboard')

    return render(
        request,
        "admin/adminlogin.html"
    )

# --------------------------------------------------------------------------------
# ----------------------------+ Admin Dashboard +---------------------------------
# --------------------------------------------------------------------------------


@seller_required
def dashboard(request):
    if not request.user.is_seller:
        return redirect('home')
    products = Product.objects.all()
    return render(request, 'admin/dashboard.html', {"products": products})


# -------------------------------+ Logout +---------------------------------------

@seller_required
def logout(request):
    auth_logout(request)
    return redirect('home')

# --------------------------------------------------------------------------------
# ------------------+ Admin Product for View Product Collection +-----------------
# --------------------------------------------------------------------------------


@seller_required
def viewpro(request):
    return render(request, "admin/viewproduct.html")

# --------------------------------------------------------------------------------
# ---------------------------+ Show Order +---------------------------------------
# --------------------------------------------------------------------------------
@seller_required
def order(request):
    orders = Order.objects.select_related(
        'user',
        'product'
    )

    return render(
        request,
        'admin/order.html',
        {'orders': orders}
    )

# --------------------------------------------------------------------------------
# -------------------------+ Admin Add Product +----------------------------------
# --------------------------------------------------------------------------------


@seller_required
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
        'admin/addpro.html', {'form': form})


# --------------------------------------------------------------------------------
# ---------------------------+  Edit Product Stock +------------------------------
# --------------------------------------------------------------------------------
@seller_required
def editstock(request, name):

    product = get_object_or_404(
        Product,
        name=name
    )

    if request.method == 'POST':
        product.stock = request.POST.get("stock")
        product.save()

        if product.category == "Dress":
            return redirect('admin_dress')

        elif product.category == "Saree":
            return redirect('admin_saree')

        elif product.category == "Heels":
            return redirect('admin_heals')

        elif product.category == "Shoes":
            return redirect('admin_shoes')

        elif product.category == "Shirt":
            return redirect('admin_shirt')

        elif product.category == "Pant":
            return redirect('admin_pant')

        elif product.category == "Jewellery":
            return redirect('admin_jewellery')

        elif product.category == "Footwear":
            return redirect('admin_footwear')

    return render(
        request,
        "admin/editstock.html",
        {
            "product": product
        }
    )


# --------------------------------------------------------------------------------
# ------------------------------+ Edit Product +----------------------------------
# --------------------------------------------------------------------------------
@seller_required
def editproduct(request, name):

    product = get_object_or_404(Product, name=name)

    if request.method == 'POST':
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.mainprice = request.POST.get("mainprice")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.save()

        return redirect('dashboard')

    return render(
        request,
        "admin/editproduct.html",
        {
            "product": product
        }
    )
# --------------------------------------------------------------------------------
# --------------------- Admin Product for View Shtock ----------------------------
# --------------------------------------------------------------------------------


@seller_required
def admin_dress(request):
    products = Product.objects.filter(
        category='dress'
    )
    return render(
        request,
        'adminproducts/dress.html',
        {
            'products': products
        }
    )


@seller_required
def admin_saree(request):
    products = Product.objects.filter(
        category='Saree'
    )
    return render(
        request,
        'adminproducts/saree.html',
        {
            'products': products
        }
    )


@seller_required
def admin_heels(request):
    products = Product.objects.filter(
        category='Heals'
    )
    return render(
        request,
        'adminproducts/heels.html',
        {
            'products': products
        }
    )


@seller_required
def admin_jwelery(request):
    products = Product.objects.filter(
        category='Jwelery'
    )
    return render(
        request,
        'adminproducts/jwelery.html',
        {
            'products': products
        }
    )


@seller_required
def admin_foowear(request):
    products = Product.objects.filter(
        category='Footwear'
    )
    return render(
        request,
        'adminproducts/footwear.html',
        {
            'products': products
        }
    )


@seller_required
def admin_pent(request):
    products = Product.objects.filter(
        category='Pent'
    )
    return render(
        request,
        'adminproducts/pent.html',
        {
            'products': products
        }
    )


@seller_required
def admin_shert(request):
    products = Product.objects.filter(
        category='Shert'
    )
    return render(
        request,
        'adminproducts/shert.html',
        {
            'products': products
        }
    )


@seller_required
def admin_shoes(request):

    products = Product.objects.filter(
        category='Shoes'
    )
    return render(
        request,
        'adminproducts/shoes.html',
        {
            'products': products
        }
    )
