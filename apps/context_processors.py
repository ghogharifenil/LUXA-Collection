from .models import Cart
from django.db.models import Sum

def cart_count(request):

    if request.session.get('customer_id'):

        customer_id = request.session.get('customer_id')

        count = Cart.objects.filter(
            customer_id=customer_id
        ).aggregate(
            total=Sum('quantity')
        )['total'] or 0

    else:
        count = 0

    return {
        'cart_count': count
    }