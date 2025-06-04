from django import forms
from .models import Product



class ListingForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'price', 'stock', 'sizes', 'available', 'category']
        
        
        widgets = {
            'sizes': forms.CheckboxSelectMultiple()
        }
        
class ProductFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
    ]
    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False)
