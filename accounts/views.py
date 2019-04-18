from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

# User 모델을 가져오는 방법
# from django.contrib.auth.models import User
# from django.conf import settings  ==> settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm
from .forms import ProfileForm
from .models import Profile


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auth_login(request, form.get_user())
            # 가입된 유저의 Profile 레코드 함께 생성
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:list')
    else:
        form = CustomUserCreationForm()
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
    
    
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('accounts:signup')
    else:
        return render(request, 'accounts/delete.html')
        

@login_required
def follow(request, user_id):
    person = get_object_or_404(get_user_model(), pk=user_id)
    if request.user in person.followers.all():
        person.followers.remove(request.user)
    else:
        print(person)
        person.followers.add(request.user)
    return redirect('profile', person.username)
    

@login_required
def change_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile', request.user.username)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        context = {
            'profile_form': profile_form,
        }
    return render(request, 'accounts/change_profile.html', context)