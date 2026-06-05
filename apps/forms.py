from django import forms
from .models import Product
from .models import User

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'category',
            'name',
            'price',
            'description',
            'image',
            'mainprice',
            'stock',
            'tags',
        ]

        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product Name'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product Price'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Product Description',
                'rows': 4
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),

            'mainprice': forms.NumberInput(attrs={
                'class': 'old-price',
                'placeholder': 'Old Price'
            }),
            
            'stock': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Storing Stock '
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add Tags'
            }),
        }


class CustomerRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'city', 'password']