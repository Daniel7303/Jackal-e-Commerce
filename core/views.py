from django.shortcuts import render
from django.shortcuts import HttpResponse
from markets.models import Product, Wishlist
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.


def home(request, category=None):
    lists = Product.objects.all()
    paginator = Paginator(lists, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    wishlisted_ids = []
    if request.user.is_authenticated:
        wishlisted_ids = Wishlist.objects.filter(user=request.user).values_list('product_id', flat=True)
        
    

    return render(request, 'core/home.html', {
        'page_obj': page_obj,
        'wishlisted_ids': wishlisted_ids,
        'lists': lists,
    })
    
    
    
def product_items(request):
    query = request.GET.get('query')
    
    lists = Product.objects.all()
    
    paginator = Paginator(lists, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    if query:
        posts = lists.filter(Q(title__icontains=query) | Q(description__icontains=query))
        messages.info(request, f"{posts.count()} result(s) found")
        
    else:
        posts = lists
    
    
    return render(request, 'core/items.html', {'lists':posts, 'page_obj': page_obj})
