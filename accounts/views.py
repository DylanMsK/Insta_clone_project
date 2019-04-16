from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

# User 모델을 가져오는 방법
# from django.contrib.auth.models import User
# from django.conf import settings  ==> settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auth_login(request, form.get_user())
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = UserCreationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/signup.html', context)
        
    
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        print(form)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('posts:list')
    else:
        form = AuthenticationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/login.html', context)


def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    
    
def profile(request, username):
    profile = get_object_or_404(get_user_model(), username=username)
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)