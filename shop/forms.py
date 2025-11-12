from django import forms
from shop.models import Product, ProductRating


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'stock']
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image size should be less than 10MB")
            return image
        return None


class ProductRatingForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5)
    
    class Meta:
        model = ProductRating
        fields = ['rating', 'review']