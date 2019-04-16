from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


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