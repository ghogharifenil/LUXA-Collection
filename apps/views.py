from django.contrib.auth.hashers import check_password
from .forms import ProductForm
from .models import Product
from .models import Order
from .models import contectmassage
from .models import CustomerModel
from .models import Cart
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from .decorators import seller_required, customer_login_required
from django.db.models import Q
from .forms import CustomerRegisterForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .models import contectmassage
# --------------------------------------------------------------------------------
# --------------------+ Main Page Of LUXA Collection +----------------------------
# --------------------------------------------------------------------------------


def luxa(request):
    return render(request, "html/luxa.html")

# ---------------+ Home Page +----------------------------


def home(request):
    return render(request, "html/home.html")


def about(request):
    return render(request, "html/about.html")


@customer_login_required
def contectus(request):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("customer_login")

    customer = CustomerModel.objects.get(id=customer_id)

    if request.method == "POST":

        subject = request.POST.get("subject")
        message = request.POST.get("message")

        contectmassage.objects.create(
            user=customer,
            subject=subject,
            message=message
        )

        return redirect("contectus")

    return render(
        request,
        "html/contectus.html",
        {
            "customer": customer
        }
    )

# ---------------+ Serch Bar +----------------------------


def search_product(request):
    query = request.GET.get('q', '').strip()

    products = Product.objects.none()

    if query:
        words = query.split()

        q_filter = Q()

        for word in words:
            q_filter &= (
                Q(name__icontains=word) |
                Q(tags__icontains=word) |
                Q(description__icontains=word)
            )

        products = Product.objects.filter(q_filter)

    context = {
        'products': products,
        'query': query
    }

    return render(request, 'html/search.html', context)

# ---------------+ New Collection Department +----------------


def new_products(request):

    products = Product.objects.filter(
        is_new=True
    )

    return render(
        request,
        'html/new_collection.html',
        {'products': products}
    )
# ---------------+ Add to Cart With Login  +----------------


@customer_login_required
def cart(request):

    customer_id = request.session.get("customer_id")

    items = Cart.objects.filter(
        customer_id=customer_id
    )

    subtotal = 0

    for item in items:
        subtotal += float(item.product.price) * item.quantity

    shipping = 99 if subtotal > 0 else 0

    total = subtotal + shipping

    return render(
        request,
        "html/add_to_cart.html",
        {
            "items": items,
            "subtotal": subtotal,
            "shipping": shipping,
            "total": total
        }
    )


@customer_login_required
def add_to_cart(request, product_name):

    customer_id = request.session.get("customer_id")

    if not customer_id:
        return redirect("login")

    product = get_object_or_404(Product, name=product_name)

    cart_item = Cart.objects.filter(
        customer_id=customer_id,
        product=product
    ).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            customer_id=customer_id,
            product=product,
            quantity=1
        )

    # 🔥 BUY NOW CHECK
    if request.GET.get("buy") == "1":
        return redirect("checkout")

    # default
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@customer_login_required
def increase_qty(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    item.quantity += 1
    item.save()

    customer_id = request.session.get("customer_id")

    items = Cart.objects.filter(customer_id=customer_id)

    subtotal = sum(
        float(i.product.price) * i.quantity
        for i in items
    )

    shipping = 99 if subtotal > 0 else 0
    total = subtotal + shipping

    return JsonResponse({
        "quantity": item.quantity,
        "item_total": float(item.product.price) * item.quantity,
        "subtotal": subtotal,
        "total": total
    })


@customer_login_required
def decrease_qty(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    customer_id = request.session.get("customer_id")

    items = Cart.objects.filter(customer_id=customer_id)

    subtotal = sum(
        float(i.product.price) * i.quantity
        for i in items
    )

    shipping = 99 if subtotal > 0 else 0
    total = subtotal + shipping

    return JsonResponse({
        "quantity": item.quantity,
        "item_total": float(item.product.price) * item.quantity,
        "subtotal": subtotal,
        "total": total
    })


@customer_login_required
def remove_cart(request, cart_id):

    customer_id = request.session.get('customer_id')

    item = get_object_or_404(
        Cart,
        id=cart_id,
        customer_id=customer_id
    )

    item.delete()

    remaining_items = Cart.objects.filter(
        customer_id=customer_id
    )

    subtotal = sum(
        item.product.price * item.quantity
        for item in remaining_items
    )

    shipping = 99 if subtotal > 0 else 0
    total = subtotal + shipping

    return JsonResponse({
        "success": True,
        "subtotal": subtotal,
        "total": total
    })


@customer_login_required
def cart_count(request):

    count = 0

    customer_id = request.session.get(
        "customer_id"
    )

    if customer_id:
        count = Cart.objects.filter(
            customer_id=customer_id
        ).count()

    return {
        "cart_count": count
    }


def send_order_email(customer_id, name, orders, total):

    user_email = CustomerModel.objects.get(id=customer_id).email

    subject = "🛍️ Your Order Confirmed - LUXA Collection"

    html_content = render_to_string("html/sendmail.html", {
        "name": name,
        "orders": orders,
        "total": total
    })

    email = EmailMultiAlternatives(
        subject,
        "",
        settings.EMAIL_HOST_USER,
        [user_email]
    )

    email.attach_alternative(html_content, "text/html")
    email.send()


@customer_login_required
def checkout(request):

    customer_id = request.session.get('customer_id')
    cart_items = Cart.objects.filter(customer_id=customer_id)

    if not cart_items.exists():
        return redirect('cart')

    subtotal = sum(item.total_price for item in cart_items)
    shipping = 99
    total = subtotal + shipping

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        orders = []   # 🔥 FIX 1: list banavyo

        # create orders
        for item in cart_items:
            order = Order.objects.create(
                user_id=customer_id,
                product=item.product,
                quantity=item.quantity,
                total_price=item.total_price,
            )
            orders.append(order)   # 🔥 FIX 2

        # clear cart
        cart_items.delete()

        # 🔥 FIX 3: correct total pass
        send_order_email(customer_id, name, orders, total)

        return redirect('home')

    return render(request, 'html/checkout.html', {
        'items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })


def register(request):
    if request.method == "POST":
        form = CustomerRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.password = make_password(
                form.cleaned_data["password"]
            )

            user.save()

            return redirect("login")

    else:
        form = CustomerRegisterForm()

    return render(request, "html/registration.html", {"form": form})


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = CustomerModel.objects.get(email=email)

            if check_password(password, user.password):

                request.session["customer_id"] = user.id
                request.session["customer_name"] = user.name

                return redirect("home")

            else:
                messages.error(request, "Invalid Password")

        except CustomerModel.DoesNotExist:
            messages.error(request, "Email Not Found")

    return render(request, "html/customer_login.html")


def customerlogout(request):
    request.session.flush()
    return redirect("home")

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

# # @customer_login_required
# def adminuser(request):

#     if request.method == 'POST':

#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         user = authenticate(
#             request,
#             email=email,
#             password=password
#         )

#         if user is not None and user.is_superuser:
#             auth_login(request, user)
#             return redirect('dashboard')

#     return render(
#         request,
#         "admin/adminlogin.html"
#     )

def adminuser(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user:
            auth_login(request, user)
            return redirect('dashboard')

        return render(request, "admin/adminlogin.html", {
            "error": "Invalid email or password"
        })

    return render(request, "admin/adminlogin.html")

# --------------------------------------------------------------------------------
# ----------------------------+ Admin Dashboard +---------------------------------
# --------------------------------------------------------------------------------



def dashboard(request):
    products = Product.objects.all()
    return render(request, 'admin/dashboard.html', {"products": products})

# -------------------------------+ Logout +---------------------------------------

@seller_required
def logout(request):
    auth_logout(request)
    return redirect('admin')

# --------------------------------------------------------------------------------
# ------------------+ Admin Product for View Product Collection +-----------------
# --------------------------------------------------------------------------------


@seller_required
def contact_messages(request):
    messages = contectmassage.objects.all().order_by('-id')

    return render(
        request,
        "admin/contact_messages.html",
        {"messages": messages}
    )


@seller_required
def resolve_message(request, id):

    msg = get_object_or_404(contectmassage, id=id)

    send_mail(
        subject="LUXA Collection - Support Update",
        message=f"""
Hello {msg.user.name},

Thank you for contacting LUXA Collection.

We have received your message regarding:

{msg.subject}

Our support team is currently working on your request and will get back to you as soon as possible.

Thank you for your patience.

LUXA Collection Team
        """,
        from_email="luxacollection@gmail.com",
        recipient_list=[msg.user.email],
        fail_silently=False,
    )

    msg.is_resolved = True
    msg.save()

    return redirect("contact_messages")
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


def mark_shipped(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    order.is_shipped = True
    order.save()

    # email send
    send_mail(
        subject="Your Order is Shipped 🚚",
        message=f"""
Hi {order.user.name},

Your product "{order.product.name}" is now shipped.
Please collect it within 24 hours.

Thank you for shopping with LUXA Collection.
""",
        from_email="yourshop@gmail.com",
        recipient_list=[order.user.email],
        fail_silently=False,
    )

    return redirect('order')
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

            product = form.save(commit=False)

            product.is_new = True if request.POST.get("is_new") else False

            product.save()

            return redirect('add_product')

    else:
        form = ProductForm()

    return render(
        request,
        'admin/addpro.html', {'form': form})


@customer_login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product.delete()

    return redirect('dashboard')

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
        category='Dress'
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
