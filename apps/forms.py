from django import forms
from .models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'category',
            'name',
            'price',
            'description',
            'image'
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
        }