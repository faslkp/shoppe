from django.shortcuts import render
from django.shortcuts import redirect

from users.forms import UserRegistrationForm

def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            return redirect('shop:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', {'form': form})


def user_login(request):
    pass

def user_logout(request):
    pass


def user_cart(request):
    pass