from django.contrib import admin
from . models import Product
from .models import Size
from .models import Wishlist


# Register your models here.

admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Wishlist)
