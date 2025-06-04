
# from decimal import Decimal
# from django.conf import settings

from markets.models import Product


def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modidied = True
    

def add_to_cart(request, product_id, quantity):
    cart = get_cart(request)
    product_id = str(product_id)
    quantity = int(quantity)
    
    if product_id in cart:
        cart[product_id] += quantity
    
    else:
        cart[product_id] = quantity
    
    save_cart(request, cart)


def remove_from_cart(request, product_id):
    cart = get_cart(request)
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        save_cart(request, cart)

def get_cart_items(request):
    cart = get_cart(request)
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return items, total