from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from users.models import Address

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        placeholders = {
            'name': 'Full Name',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        for field_name, field in self.fields.items():
            field.help_text = ''
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        for field_name, field in self.fields.items():
            field.help_text = ''
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing_classes + ' form-control').strip()



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2', 'city', 'state', 'zip_code', 'country']