from django.shortcuts import render, redirect
from . models import Product, Wishlist, Cart, CartItem
from .forms import ListingForm
from .forms import ProductFilterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

# from .cart import add_to_cart, get_cart_items, remove_from_cart
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Order, OrderItem
from decimal import Decimal





# Create your views here.
@login_required
def add_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            form.save_m2m()
            return redirect('core:home')
    
    else:
        form = ListingForm()
    return render(request, 'markets/create_listings.html', {'form':form})



def list_page(request, category=None):
    categories = request.GET.getlist('category')
    sizes = request.GET.getlist('size')

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    if categories:
        products = products.filter(category__in=categories)

    if sizes:
        products = products.filter(sizes__name__in=sizes).distinct()

    context = {
        'lists': products,
        'selected_categories': categories,
        'selected_sizes': sizes,
        'selected_category': category,
    }
    return render(request, 'core/items.html', context, {'show_search': True})




def item_details(request, slug):
    item = get_object_or_404(Product, slug=slug)
    return render(request, 'markets/item_details.html', {'item': item})




def add_to_cart_view(request, product_id):
    if request.method == "POST":
        item = Product.objects.get(id=product_id)
            
        if request.user.is_authenticated:
            if item.stock == 0:
                messages.error(request, "This item is currently out of stock.")
                return redirect('market:item_details', slug=item.slug)
            
            quantity = int(request.POST.get("quantity", 1))
            
            if quantity > item.stock:
                messages.error(request, f"Only {item.stock} item(s) left in stock.")
                return redirect('market:item_details', slug=item.slug)
            
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=item)
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Item added to cart successfully!")
            Wishlist.objects.filter(user=request.user, product=item).delete()
        
            
            return redirect('market:item_details', slug=item.slug)
        else:
            messages.success(request, "Please Register/Login to add item to Cart!")
            return redirect('market:item_details', slug=item.slug)
    

def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    for item in items:
        item.subtotal = item.product.price * item.quantity
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'markets/cart.html', {'items': items, 'total': total, 'show_search': True})


def remove_from_cart_view(request, product_id):
    cart = Cart.objects.get(user=request.user)
    CartItem.objects.filter(cart=cart, product_id=product_id).delete()
    
    return redirect('market:cart_view')




# wishlists

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    

    if created:
        messages.success(request, "Item added to wishlist.")
    else:
        wishlist_item.delete()
        messages.info(request, "Item removed from wishlist.")

    return redirect(request.META.get('HTTP_REFERER', 'market:home'))

        
    

def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('market:view_wishlist')



def view_wishlist(request):
    if request.user.is_authenticated:
        wishlists = Wishlist.objects.filter(user=request.user)
    else:
        return redirect('account:register')

    return render(request, 'markets/wishlist.html', {'wishlists':wishlists, 'show_search': False})



def order_summary(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('market:product_list')

    items = cart.items.select_related('product')  # optimize DB query

    subtotal = Decimal(0)
    for item in items:
        if item.product and item.product.price:
            item.subtotal = item.product.price * item.quantity
            subtotal += item.product.price * item.quantity

    shipping = Decimal('5.00')
    total = subtotal + shipping

    return render(request, 'markets/summary.html', {
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    })




def checkout(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.error(request, "No items in cart.")
        return redirect('market:listings')

    total = sum(item.product.price * item.quantity for item in cart.items.all())
    order = Order.objects.create(user=request.user, total_price=total)

    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
        item.product.stock -= item.quantity
        item.product.save()

    cart.items.all().delete()
    # messages.success(request, "Order placed successfully!")
    return render(request, "markets/checkout.html", {'order_id': order.id})

