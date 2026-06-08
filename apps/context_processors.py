from .models import Cart

def cart_count(request):
    if request.session.get('customer_id'):
        customer_id = request.session.get('customer_id')
        count = Cart.objects.filter(customer_id=customer_id).count()
    else:
        count = 0

    return {
        'cart_count': count
    }