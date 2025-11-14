from django import forms
from shop.models import Product, ProductRating


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            css_classes = visible.field.widget.attrs.get('class', '')
            if not isinstance(visible.field.widget, forms.FileInput):
                visible.field.widget.attrs['class'] = f'{css_classes} form-control'.strip()
            else:
                visible.field.widget.attrs['class'] = f'{css_classes} form-control-file'.strip()
            visible.field.widget.attrs['placeholder'] = visible.field.label

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