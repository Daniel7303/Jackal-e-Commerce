from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_items, name='product_items'),
    # path('category/<str:category>/', views.home, name='category_filter'),
]