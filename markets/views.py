from django.shortcuts import render, redirect
from . models import Product, Wishlist
from .forms import ListingForm
from .forms import ProductFilterForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .cart import add_to_cart, get_cart_items, remove_from_cart
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages





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


# views.py
def list_page(request, category=None):
    if category:
        lists = Product.objects.filter(category=category)
    else:
        lists = Product.objects.all()
    return render(request, 'core/items.html', {'lists': lists, 'selected_category': category})

    

# def posts_by_category(request, category):
#     filtered_posts = Post.objects.filter(category=category)
#     categories = Post.objects.values_list('category', flat=True).distinct()
#     return render(request, 'main/category.html', {'posts': filtered_posts, 'categories': categories})


def item_details(request, slug):
    item = get_object_or_404(Product, slug=slug)
    return render(request, 'markets/item_details.html', {'item': item})




def add_to_cart_view(request, product_id):
    if request.method == "POST":
        item = Product.objects.get(id=product_id)
        if request.user.is_authenticated:
            quantity = int(request.POST.get("quantity", 1))
            add_to_cart(request, product_id, quantity)
            messages.success(request, "Item added to cart successfully!")
        
            
            return redirect('market:item_details', slug=item.slug)
        else:
            messages.success(request, "Please Register/Login to add item to Cart!")
            return redirect('market:item_details', slug=item.slug)
    

def cart_view(request):
    items, total = get_cart_items(request)
    return render(request, 'markets/cart.html', {'items': items, 'total': total})

def remove_from_cart_view(request, product_id):
    remove_from_cart(request, product_id)
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

    return render(request, 'markets/wishlist.html', {'wishlists':wishlists})


def wishlist_count(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'wishlist_count': count}