from . import views
from django.urls import path

app_name = 'market'

urlpatterns = [
    path('create/', views.add_listing, name='create_listings'),
    path('items/', views.list_page, name='listings'),
    path('market/<slug:slug>', views.item_details, name='item_details'),
    
    
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    
    
    path('category/<str:category>/', views.list_page, name='category_filter'),
    
    
    path('wishlist/add/', views.view_wishlist, name='view_wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    
    path('summary/', views.order_summary, name='order_summary'),
    path('checkout/', views.checkout, name='checkout'),
       
]

