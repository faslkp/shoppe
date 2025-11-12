from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout

from users.forms import UserRegistrationForm, UserLoginForm

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
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('shop:index')
    else:
        form = UserLoginForm(request)
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('shop:index')


def user_profile(request):
    pass


def user_cart(request):
    pass